# PIX2PIX Translation
def pix2pix_translation():
  p2pt = """
  from download import download

  url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/models/application/dataset_pix2pix.tar"

  download(url, "./dataset", kind="tar", replace=True)

  from mindspore import dataset as ds
  import matplotlib.pyplot as plt

  dataset = ds.MindDataset("./dataset_pix2pix/train.mindrecord", columns_list=["input_images", "target_images"], shuffle=True)
  data_iter = next(dataset.create_dict_iterator(output_numpy=True))
  # Visualize some training data.
  plt.figure(figsize=(10, 3), dpi=140)
  for i, image in enumerate(data_iter['input_images'][:10], 1):
      plt.subplot(3, 10, i)
      plt.axis("off")
      plt.imshow((image.transpose(1, 2, 0) + 1) / 2)
  plt.show()

  import mindspore
  import mindspore.nn as nn
  import mindspore.ops as ops

  class UNetSkipConnectionBlock(nn.Cell):
      def __init__(self, outer_nc, inner_nc, in_planes=None, dropout=False,
                  submodule=None, outermost=False, innermost=False, alpha=0.2, norm_mode='batch'):
          super(UNetSkipConnectionBlock, self).__init__()
          down_norm = nn.BatchNorm2d(inner_nc)
          up_norm = nn.BatchNorm2d(outer_nc)
          use_bias = False
          if norm_mode == 'instance':
              down_norm = nn.BatchNorm2d(inner_nc, affine=False)
              up_norm = nn.BatchNorm2d(outer_nc, affine=False)
              use_bias = True
          if in_planes is None:
              in_planes = outer_nc
          down_conv = nn.Conv2d(in_planes, inner_nc, kernel_size=4,
                                stride=2, padding=1, has_bias=use_bias, pad_mode='pad')
          down_relu = nn.LeakyReLU(alpha)
          up_relu = nn.ReLU()
          if outermost:
              up_conv = nn.Conv2dTranspose(inner_nc * 2, outer_nc,
                                          kernel_size=4, stride=2,
                                          padding=1, pad_mode='pad')
              down = [down_conv]
              up = [up_relu, up_conv, nn.Tanh()]
              
              # Looking at the U-Net generartor class below, the layers are made up of this UNetSkipConnection Class,
              # which is essential in the decoder(upsampling) section but throughout this if statement, they used this model = ...
              # in the line below to build up a Conv2D layer together with a Conv2DTranspose layer make it look like they built
              # only the decoder section with the 'model' variable
              
              model = down + [submodule] + up
          elif innermost:
              up_conv = nn.Conv2dTranspose(inner_nc, outer_nc,
                                          kernel_size=4, stride=2,
                                          padding=1, has_bias=use_bias, pad_mode='pad')
              down = [down_relu, down_conv]
              up = [up_relu, up_conv, up_norm]
              model = down + up
          else:
              up_conv = nn.Conv2dTranspose(inner_nc * 2, outer_nc,
                                          kernel_size=4, stride=2,
                                          padding=1, has_bias=use_bias, pad_mode='pad')
              down = [down_relu, down_conv, down_norm]
              up = [up_relu, up_conv, up_norm]

              model = down + [submodule] + up
              if dropout:
                  model.append(nn.Dropout(p=0.5))
          self.model = nn.SequentialCell(model)
          self.skip_connections = not outermost

      def construct(self, x):
          out = self.model(x)
          if self.skip_connections:
              out = ops.concat((out, x), axis=1)
          return out

  class UNetGenerator(nn.Cell):
      def __init__(self, in_planes, out_planes, ngf=64, n_layers=8, norm_mode='bn', dropout=False):
          super(UNetGenerator, self).__init__()
          unet_block = UNetSkipConnectionBlock(ngf * 8, ngf * 8, in_planes=None, submodule=None,
                                              norm_mode=norm_mode, innermost=True)
          for _ in range(n_layers - 5):
              unet_block = UNetSkipConnectionBlock(ngf * 8, ngf * 8, in_planes=None, submodule=unet_block,
                                                  norm_mode=norm_mode, dropout=dropout)
          unet_block = UNetSkipConnectionBlock(ngf * 4, ngf * 8, in_planes=None, submodule=unet_block,
                                              norm_mode=norm_mode)
          unet_block = UNetSkipConnectionBlock(ngf * 2, ngf * 4, in_planes=None, submodule=unet_block,
                                              norm_mode=norm_mode)
          unet_block = UNetSkipConnectionBlock(ngf, ngf * 2, in_planes=None, submodule=unet_block,
                                              norm_mode=norm_mode)
          self.model = UNetSkipConnectionBlock(out_planes, ngf, in_planes=in_planes, submodule=unet_block,
                                              outermost=True, norm_mode=norm_mode)

      def construct(self, x):
          return self.model(x)

  import mindspore.nn as nn

  class ConvNormRelu(nn.Cell):
      def __init__(self,
                  in_planes,
                  out_planes,
                  kernel_size=4,
                  stride=2,
                  alpha=0.2,
                  norm_mode='batch',
                  pad_mode='CONSTANT',
                  use_relu=True,
                  padding=None):
          super(ConvNormRelu, self).__init__()
          norm = nn.BatchNorm2d(out_planes)
          if norm_mode == 'instance':
              norm = nn.BatchNorm2d(out_planes, affine=False)
          has_bias = (norm_mode == 'instance')
          if not padding:
              padding = (kernel_size - 1) // 2
          if pad_mode == 'CONSTANT':
              conv = nn.Conv2d(in_planes, out_planes, kernel_size, stride, pad_mode='pad',
                              has_bias=has_bias, padding=padding)
              layers = [conv, norm]
          else:
              paddings = ((0, 0), (0, 0), (padding, padding), (padding, padding))
              pad = nn.Pad(paddings=paddings, mode=pad_mode)
              conv = nn.Conv2d(in_planes, out_planes, kernel_size, stride, pad_mode='pad', has_bias=has_bias)
              layers = [pad, conv, norm]
          if use_relu:
              relu = nn.ReLU()
              if alpha > 0:
                  relu = nn.LeakyReLU(alpha)
              layers.append(relu)
          self.features = nn.SequentialCell(layers)

      def construct(self, x):
          output = self.features(x)
          return output

  class Discriminator(nn.Cell):
      def __init__(self, in_planes=3, ndf=64, n_layers=3, alpha=0.2, norm_mode='batch'):
          super(Discriminator, self).__init__()
          kernel_size = 4
          layers = [
              nn.Conv2d(in_planes, ndf, kernel_size, 2, pad_mode='pad', padding=1),
              nn.LeakyReLU(alpha)
          ]
          nf_mult = ndf
          for i in range(1, n_layers):
              nf_mult_prev = nf_mult
              nf_mult = min(2 ** i, 8) * ndf
              layers.append(ConvNormRelu(nf_mult_prev, nf_mult, kernel_size, 2, alpha, norm_mode, padding=1))
          nf_mult_prev = nf_mult
          nf_mult = min(2 ** n_layers, 8) * ndf
          layers.append(ConvNormRelu(nf_mult_prev, nf_mult, kernel_size, 1, alpha, norm_mode, padding=1))
          layers.append(nn.Conv2d(nf_mult, 1, kernel_size, 1, pad_mode='pad', padding=1))
          self.features = nn.SequentialCell(layers)

      def construct(self, x, y):
          x_y = ops.concat((x, y), axis=1)
          output = self.features(x_y)
          return output

  import mindspore.nn as nn
  from mindspore.common import initializer as init

  g_in_planes = 3
  g_out_planes = 3
  g_ngf = 64
  g_layers = 8
  d_in_planes = 6
  d_ndf = 64
  d_layers = 3
  alpha = 0.2
  init_gain = 0.02
  init_type = 'normal'


  net_generator = UNetGenerator(in_planes=g_in_planes, out_planes=g_out_planes,
                                ngf=g_ngf, n_layers=g_layers)
  for _, cell in net_generator.cells_and_names():
      if isinstance(cell, (nn.Conv2d, nn.Conv2dTranspose)):
          if init_type == 'normal':
              cell.weight.set_data(init.initializer(init.Normal(init_gain), cell.weight.shape))
          elif init_type == 'xavier':
              cell.weight.set_data(init.initializer(init.XavierUniform(init_gain), cell.weight.shape))
          elif init_type == 'constant':
              cell.weight.set_data(init.initializer(0.001, cell.weight.shape))
          else:
              raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
      elif isinstance(cell, nn.BatchNorm2d):
          cell.gamma.set_data(init.initializer('ones', cell.gamma.shape))
          cell.beta.set_data(init.initializer('zeros', cell.beta.shape))


  net_discriminator = Discriminator(in_planes=d_in_planes, ndf=d_ndf,
                                    alpha=alpha, n_layers=d_layers)
  for _, cell in net_discriminator.cells_and_names():
      if isinstance(cell, (nn.Conv2d, nn.Conv2dTranspose)):
          if init_type == 'normal':
              cell.weight.set_data(init.initializer(init.Normal(init_gain), cell.weight.shape))
          elif init_type == 'xavier':
              cell.weight.set_data(init.initializer(init.XavierUniform(init_gain), cell.weight.shape))
          elif init_type == 'constant':
              cell.weight.set_data(init.initializer(0.001, cell.weight.shape))
          else:
              raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
      elif isinstance(cell, nn.BatchNorm2d):
          cell.gamma.set_data(init.initializer('ones', cell.gamma.shape))
          cell.beta.set_data(init.initializer('zeros', cell.beta.shape))

  class Pix2Pix(nn.Cell):
      def __init__(self, discriminator, generator):
          super(Pix2Pix, self).__init__(auto_prefix=True)
          self.net_discriminator = discriminator
          self.net_generator = generator

      def construct(self, reala):
          fakeb = self.net_generator(reala)
          return fakeb

  import numpy as np
  import os
  import datetime
  from mindspore import value_and_grad, Tensor

  epoch_num = 100
  ckpt_dir = "results/ckpt"
  dataset_size = 400
  val_pic_size = 256
  lr = 0.0002
  n_epochs = 100
  n_epochs_decay = 100

  def get_lr():
      lrs = [lr] * dataset_size * n_epochs
      lr_epoch = 0
      for epoch in range(n_epochs_decay):
          lr_epoch = lr * (n_epochs_decay - epoch) / n_epochs_decay
          lrs += [lr_epoch] * dataset_size
      lrs += [lr_epoch] * dataset_size * (epoch_num - n_epochs_decay - n_epochs)
      return Tensor(np.array(lrs).astype(np.float32))

  dataset = ds.MindDataset("./dataset_pix2pix/train.mindrecord", columns_list=["input_images", "target_images"], shuffle=True, num_parallel_workers=16)
  steps_per_epoch = dataset.get_dataset_size()
  loss_f = nn.BCEWithLogitsLoss()
  l1_loss = nn.L1Loss()

  def forword_dis(reala, realb):
      lambda_dis = 0.5
      fakeb = net_generator(reala)
      pred0 = net_discriminator(reala, fakeb)
      pred1 = net_discriminator(reala, realb)
      loss_d = loss_f(pred1, ops.ones_like(pred1)) + loss_f(pred0, ops.zeros_like(pred0))
      loss_dis = loss_d * lambda_dis
      return loss_dis

  def forword_gan(reala, realb):
      lambda_gan = 0.5
      lambda_l1 = 100
      fakeb = net_generator(reala)
      pred0 = net_discriminator(reala, fakeb)
      loss_1 = loss_f(pred0, ops.ones_like(pred0))
      loss_2 = l1_loss(fakeb, realb)
      loss_gan = loss_1 * lambda_gan + loss_2 * lambda_l1
      return loss_gan

  d_opt = nn.Adam(net_discriminator.trainable_params(), learning_rate=get_lr(),
                  beta1=0.5, beta2=0.999, loss_scale=1)
  g_opt = nn.Adam(net_generator.trainable_params(), learning_rate=get_lr(),
                  beta1=0.5, beta2=0.999, loss_scale=1)

  grad_d = value_and_grad(forword_dis, None, net_discriminator.trainable_params())
  grad_g = value_and_grad(forword_gan, None, net_generator.trainable_params())

  def train_step(reala, realb):
      loss_dis, d_grads = grad_d(reala, realb)
      loss_gan, g_grads = grad_g(reala, realb)
      d_opt(d_grads)
      g_opt(g_grads)
      return loss_dis, loss_gan

  if not os.path.isdir(ckpt_dir):
      os.makedirs(ckpt_dir)

  g_losses = []
  d_losses = []
  data_loader = dataset.create_dict_iterator(output_numpy=True, num_epochs=epoch_num)

  for epoch in range(epoch_num):
      for i, data in enumerate(data_loader):
          start_time = datetime.datetime.now()
          input_image = Tensor(data["input_images"])
          target_image = Tensor(data["target_images"])
          dis_loss, gen_loss = train_step(input_image, target_image)
          end_time = datetime.datetime.now()
          delta = (end_time - start_time).microseconds
          if i % 2 == 0:
              print("ms per step:{:.2f}  epoch:{}/{}  step:{}/{}  Dloss:{:.4f}  Gloss:{:.4f} ".format((delta / 1000), (epoch + 1), (epoch_num), i, steps_per_epoch, float(dis_loss), float(gen_loss)))
          d_losses.append(dis_loss.asnumpy())
          g_losses.append(gen_loss.asnumpy())
      if (epoch + 1) == epoch_num:
          mindspore.save_checkpoint(net_generator, ckpt_dir + "Generator.ckpt")

  from mindspore import load_checkpoint, load_param_into_net

  param_g = load_checkpoint(ckpt_dir + "Generator.ckpt")
  load_param_into_net(net_generator, param_g)
  dataset = ds.MindDataset("./dataset/dataset_pix2pix/train.mindrecord", columns_list=["input_images", "target_images"], shuffle=True)
  data_iter = next(dataset.create_dict_iterator())
  predict_show = net_generator(data_iter["input_images"])
  plt.figure(figsize=(10, 3), dpi=140)
  for i in range(10):
      plt.subplot(2, 10, i + 1)
      plt.imshow((data_iter["input_images"][i].asnumpy().transpose(1, 2, 0) + 1) / 2)
      plt.axis("off")
      plt.subplots_adjust(wspace=0.05, hspace=0.02)
      plt.subplot(2, 10, i + 11)
      plt.imshow((predict_show[i].asnumpy().transpose(1, 2, 0) + 1) / 2)
      plt.axis("off")
      plt.subplots_adjust(wspace=0.05, hspace=0.02)
  plt.show()
  """
  print(p2pt)

## 
def resnettl():
  rntl = """
  from download import download

  dataset_url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/intermediate/Canidae_data.zip"

  download(dataset_url, "./datasets-Canidae", kind="zip", replace=True)

  batch_size = 18                             # Batch size
  image_size = 224                            # Size of training image space
  num_epochs = 10                             # Number of training cycles
  lr = 0.001                                  # Learning rate
  momentum = 0.9                              # momentum
  workers = 4                                 # Number of parallel threads

  import mindspore as ms
  import mindspore.dataset as ds
  import mindspore.dataset.vision as vision

  # Dataset directory path
  data_path_train = "./datasets-Canidae/data/Canidae/train/"
  data_path_val = "./datasets-Canidae/data/Canidae/val/"

  # Create training dataset

  def create_dataset_canidae(dataset_path, usage):
      data_set = ds.ImageFolderDataset(dataset_path,
                                      num_parallel_workers=workers,
                                      shuffle=True,)

      # Data transform operations
      mean = [0.485 * 255, 0.456 * 255, 0.406 * 255]
      std = [0.229 * 255, 0.224 * 255, 0.225 * 255]
      scale = 32

      if usage == "train":
          # Define map operations for training dataset
          trans = [
              vision.RandomCropDecodeResize(size=image_size, scale=(0.08, 1.0), ratio=(0.75, 1.333)),
              vision.RandomHorizontalFlip(prob=0.5),
              vision.Normalize(mean=mean, std=std),
              vision.HWC2CHW()
          ]
      else:
          # Define map operations for inference dataset
          trans = [
              vision.Decode(),
              vision.Resize(image_size + scale),
              vision.CenterCrop(image_size),
              vision.Normalize(mean=mean, std=std),
              vision.HWC2CHW()
          ]


      # Data mapping operations
      data_set = data_set.map(
          operations=trans,
          input_columns='image',
          num_parallel_workers=workers)


      # Batch operation
      data_set = data_set.batch(batch_size)

      return data_set


  dataset_train = create_dataset_canidae(data_path_train, "train")
  step_size_train = dataset_train.get_dataset_size()

  dataset_val = create_dataset_canidae(data_path_val, "val")
  step_size_val = dataset_val.get_dataset_size()

  data = next(dataset_train.create_dict_iterator())
  images = data["image"]
  labels = data["label"]

  print("Tensor of image", images.shape)
  print("Labels:", labels)

  import matplotlib.pyplot as plt
  import numpy as np

  # class_name corresponds to label, and labels are marked in order from smallest to largest folder strings.
  class_name = {0: "dogs", 1: "wolves"}

  plt.figure(figsize=(5, 5))
  for i in range(4):
      # Get the image and its corresponding label
      data_image = images[i].asnumpy()
      data_label = labels[i]
      # Processing images for display
      data_image = np.transpose(data_image, (1, 2, 0))
      mean = np.array([0.485, 0.456, 0.406])
      std = np.array([0.229, 0.224, 0.225])
      data_image = std * data_image + mean
      data_image = np.clip(data_image, 0, 1)
      # Display image
      plt.subplot(2, 2, i+1)
      plt.imshow(data_image)
      plt.title(class_name[int(labels[i].asnumpy())])
      plt.axis("off")

  plt.show()

  from typing import Type, Union, List, Optional
  from mindspore import nn, train
  from mindspore.common.initializer import Normal


  weight_init = Normal(mean=0, sigma=0.02)
  gamma_init = Normal(mean=1, sigma=0.02)

  class ResidualBlockBase(nn.Cell):
      expansion: int = 1  # The number of last convolutional kernels is equal to the number of first convolutional kernels

      def __init__(self, in_channel: int, out_channel: int,
                  stride: int = 1, norm: Optional[nn.Cell] = None,
                  down_sample: Optional[nn.Cell] = None) -> None:
          super(ResidualBlockBase, self).__init__()
          if not norm:
              self.norm = nn.BatchNorm2d(out_channel)
          else:
              self.norm = norm

          self.conv1 = nn.Conv2d(in_channel, out_channel,
                                kernel_size=3, stride=stride,
                                weight_init=weight_init)
          self.conv2 = nn.Conv2d(in_channel, out_channel,
                                kernel_size=3, weight_init=weight_init)
          self.relu = nn.ReLU()
          self.down_sample = down_sample

      def construct(self, x):
          identity = x  # shortcuts

          out = self.conv1(x)  # The first layer of main body: 3*3 convolutional layer
          out = self.norm(out)
          out = self.relu(out)
          out = self.conv2(out)  # The second layer of main body: 3*3 convolutional layer
          out = self.norm(out)

          if self.down_sample is not None:
              identity = self.down_sample(x)
          out += identity  # The output is the sum of the main body and the shortcuts
          out = self.relu(out)

          return out

  class ResidualBlock(nn.Cell):
      expansion = 4  # The number of last convolutional kernels is 4 times the number of first convolutional kernels

      def __init__(self, in_channel: int, out_channel: int,
                  stride: int = 1, down_sample: Optional[nn.Cell] = None) -> None:
          super(ResidualBlock, self).__init__()

          self.conv1 = nn.Conv2d(in_channel, out_channel,
                                kernel_size=1, weight_init=weight_init)
          self.norm1 = nn.BatchNorm2d(out_channel)
          self.conv2 = nn.Conv2d(out_channel, out_channel,
                                kernel_size=3, stride=stride,
                                weight_init=weight_init)
          self.norm2 = nn.BatchNorm2d(out_channel)
          self.conv3 = nn.Conv2d(out_channel, out_channel * self.expansion,
                                kernel_size=1, weight_init=weight_init)
          self.norm3 = nn.BatchNorm2d(out_channel * self.expansion)

          self.relu = nn.ReLU()
          self.down_sample = down_sample

      def construct(self, x):

          identity = x  # shortscuts

          out = self.conv1(x)  # The first layer of main body: 1*1 convolutional layer
          out = self.norm1(out)
          out = self.relu(out)
          out = self.conv2(out)  # The second layer of main body: 3*3 convolutional layer
          out = self.norm2(out)
          out = self.relu(out)
          out = self.conv3(out)  # The third layer of main body: 3*3 convolutional layer
          out = self.norm3(out)

          if self.down_sample is not None:
              identity = self.down_sample(x)

          out += identity  # The output is the sum of the main body and the shortcuts
          out = self.relu(out)

          return out

  def make_layer(last_out_channel, block: Type[Union[ResidualBlockBase, ResidualBlock]],
                channel: int, block_nums: int, stride: int = 1):
      down_sample = None  # shortcuts


      if stride != 1 or last_out_channel != channel * block.expansion:

          down_sample = nn.SequentialCell([
              nn.Conv2d(last_out_channel, channel * block.expansion,
                        kernel_size=1, stride=stride, weight_init=weight_init),
              nn.BatchNorm2d(channel * block.expansion, gamma_init=gamma_init)
          ])

      layers = []
      layers.append(block(last_out_channel, channel, stride=stride, down_sample=down_sample))

      in_channel = channel * block.expansion
      # Stacked residual network
      for _ in range(1, block_nums):

          layers.append(block(in_channel, channel))

      return nn.SequentialCell(layers)

  from mindspore import load_checkpoint, load_param_into_net


  class ResNet(nn.Cell):
      def __init__(self, block: Type[Union[ResidualBlockBase, ResidualBlock]],
                  layer_nums: List[int], num_classes: int, input_channel: int) -> None:
          super(ResNet, self).__init__()

          self.relu = nn.ReLU()
          # The first convolutional layer, with the number of input channel is 3 (color image) and the number of output channel is 64
          self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, weight_init=weight_init)
          self.norm = nn.BatchNorm2d(64)
          # Max pooling layer to reduce the size of the image
          self.max_pool = nn.MaxPool2d(kernel_size=3, stride=2, pad_mode='same')
          # Definitions of each residual network structure block
          self.layer1 = make_layer(64, block, 64, layer_nums[0])
          self.layer2 = make_layer(64 * block.expansion, block, 128, layer_nums[1], stride=2)
          self.layer3 = make_layer(128 * block.expansion, block, 256, layer_nums[2], stride=2)
          self.layer4 = make_layer(256 * block.expansion, block, 512, layer_nums[3], stride=2)
          # Average pooling layer
          self.avg_pool = nn.AvgPool2d()
          # flattern layer
          self.flatten = nn.Flatten()
          # Fully-connected layer
          self.fc = nn.Dense(in_channels=input_channel, out_channels=num_classes)

      def construct(self, x):

          x = self.conv1(x)
          x = self.norm(x)
          x = self.relu(x)
          x = self.max_pool(x)

          x = self.layer1(x)
          x = self.layer2(x)
          x = self.layer3(x)
          x = self.layer4(x)

          x = self.avg_pool(x)
          x = self.flatten(x)
          x = self.fc(x)

          return x


  def _resnet(model_url: str, block: Type[Union[ResidualBlockBase, ResidualBlock]],
              layers: List[int], num_classes: int, pretrained: bool, pretrianed_ckpt: str,
              input_channel: int):
      model = ResNet(block, layers, num_classes, input_channel)

      if pretrained:
          # Load pre-trained models
          download(url=model_url, path=pretrianed_ckpt, replace=True)
          param_dict = load_checkpoint(pretrianed_ckpt)
          load_param_into_net(model, param_dict)

      return model


  def resnet50(num_classes: int = 1000, pretrained: bool = False):
      resnet50_url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/models/application/resnet50_224_new.ckpt"
      resnet50_ckpt = "./LoadPretrainedModel/resnet50_224_new.ckpt"
      return _resnet(resnet50_url, ResidualBlock, [3, 4, 6, 3], num_classes,
                    pretrained, resnet50_ckpt, 2048)

  import mindspore as ms

  network = resnet50(pretrained=True)

  # Size of fully-connected layer input layer
  in_channels = network.fc.in_channels
  # The output channel number size is 2, same as the number of wolfdog classification
  head = nn.Dense(in_channels, 2)
  # Reset fully-connected layer
  network.fc = head

  # Average pooling layer kernel size is 7
  avg_pool = nn.AvgPool2d(kernel_size=7)
  # Reset the average pooling layer
  network.avg_pool = avg_pool

  import mindspore as ms

  # Define optimizer and loss function
  opt = nn.Momentum(params=network.trainable_params(), learning_rate=lr, momentum=momentum)
  loss_fn = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')

  # Instantiate models
  model = train.Model(network, loss_fn, opt, metrics={"Accuracy": train.Accuracy()})

  def forward_fn(inputs, targets):

      logits = network(inputs)
      loss = loss_fn(logits, targets)

      return loss

  grad_fn = ms.value_and_grad(forward_fn, None, opt.parameters)

  def train_step(inputs, targets):

      loss, grads = grad_fn(inputs, targets)
      opt(grads)

      return loss

  # Create the iterator
  data_loader_train = dataset_train.create_tuple_iterator(num_epochs=num_epochs)

  # Optimal model save path
  best_ckpt_dir = "./BestCheckpoint"
  best_ckpt_path = "./BestCheckpoint/resnet50-best.ckpt"

  import os
  import time

  # Start circuit training
  print("Start Training Loop ...")

  best_acc = 0

  for epoch in range(num_epochs):
      losses = []
      network.set_train()

      epoch_start = time.time()

      # Reads in data for each training round
      for i, (images, labels) in enumerate(data_loader_train):
          labels = labels.astype(ms.int32)
          loss = train_step(images, labels)
          losses.append(loss)

      # Verify the accuracy after each epoch

      acc = model.eval(dataset_val)['Accuracy']

      epoch_end = time.time()
      epoch_seconds = (epoch_end - epoch_start) * 1000
      step_seconds = epoch_seconds/step_size_train

      print("-" * 20)
      print("Epoch: [%3d/%3d], Average Train Loss: [%5.3f], Accuracy: [%5.3f]" % (
          epoch+1, num_epochs, sum(losses)/len(losses), acc
      ))
      print("epoch time: %5.3f ms, per step time: %5.3f ms" % (
          epoch_seconds, step_seconds
      ))

      if acc > best_acc:
          best_acc = acc
          if not os.path.exists(best_ckpt_dir):
              os.mkdir(best_ckpt_dir)
          ms.save_checkpoint(network, best_ckpt_path)

  print("=" * 80)
  print(f"End of validation the best Accuracy is: {best_acc: 5.3f}, "
        f"save the best ckpt file in {best_ckpt_path}", flush=True)

  import matplotlib.pyplot as plt
  import mindspore as ms

  def visualize_model(best_ckpt_path, val_ds):
      net = resnet50()
      # Size of fully-connected layer input layer
      in_channels = net.fc.in_channels
      # The output channel number size is 2, same as the number of wolfdog classification
      head = nn.Dense(in_channels, 2)
      # Reset fully-connected layer
      net.fc = head
      # Average pooling layer kernel size is 7
      avg_pool = nn.AvgPool2d(kernel_size=7)
      # Reset average pooling layer
      net.avg_pool = avg_pool
      # Load model parameters
      param_dict = ms.load_checkpoint(best_ckpt_path)
      ms.load_param_into_net(net, param_dict)
      model = train.Model(net)
      # Load the data from the validation set for validation
      data = next(val_ds.create_dict_iterator())
      images = data["image"].asnumpy()
      labels = data["label"].asnumpy()
      class_name = {0: "dogs", 1: "wolves"}
      # Predicted image categories
      output = model.predict(ms.Tensor(data['image']))
      pred = np.argmax(output.asnumpy(), axis=1)

      # Display images and predicted values of images
      plt.figure(figsize=(5, 5))
      for i in range(4):
          plt.subplot(2, 2, i + 1)
          # If the prediction is correct, the display is blue, and if the prediction is wrong, the display is red
          color = 'blue' if pred[i] == labels[i] else 'red'
          plt.title('predict:{}'.format(class_name[pred[i]]), color=color)
          picture_show = np.transpose(images[i], (1, 2, 0))
          mean = np.array([0.485, 0.456, 0.406])
          std = np.array([0.229, 0.224, 0.225])
          picture_show = std * picture_show + mean
          picture_show = np.clip(picture_show, 0, 1)
          plt.imshow(picture_show)
          plt.axis('off')

      plt.show()

  net_work = resnet50(pretrained=True)

  # Size of fully-connected layer input layer
  in_channels = net_work.fc.in_channels
  # The output channel number size is 2, same as the number of wolfdog classification
  head = nn.Dense(in_channels, 2)
  # Reset fully-connected layer
  net_work.fc = head

  # Average pooling layer kernel size is 7
  avg_pool = nn.AvgPool2d(kernel_size=7)
  # Reset average pooling layer
  net_work.avg_pool = avg_pool

  # Freeze all parameters except the last layer
  for param in net_work.get_parameters():
      if param.name not in ["fc.weight", "fc.bias"]:
          param.requires_grad = False

  # Define optimizer and loss function
  opt = nn.Momentum(params=net_work.trainable_params(), learning_rate=lr, momentum=0.5)
  loss_fn = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')


  def forward_fn(inputs, targets):
      logits = net_work(inputs)
      loss = loss_fn(logits, targets)

      return loss

  grad_fn = ms.value_and_grad(forward_fn, None, opt.parameters)

  def train_step(inputs, targets):
      loss, grads = grad_fn(inputs, targets)
      opt(grads)
      return loss

  # Instantiate models
  model1 = train.Model(net_work, loss_fn, opt, metrics={"Accuracy": train.Accuracy()})

  dataset_train = create_dataset_canidae(data_path_train, "train")
  step_size_train = dataset_train.get_dataset_size()

  dataset_val = create_dataset_canidae(data_path_val, "val")
  step_size_val = dataset_val.get_dataset_size()

  num_epochs = 10

  # Creating Iterators
  data_loader_train = dataset_train.create_tuple_iterator(num_epochs=num_epochs)
  data_loader_val = dataset_val.create_tuple_iterator(num_epochs=num_epochs)
  best_ckpt_dir = "./BestCheckpoint"
  best_ckpt_path = "./BestCheckpoint/resnet50-best-freezing-param.ckpt"

  # Start circuit training
  print("Start Training Loop ...")

  best_acc = 0

  for epoch in range(num_epochs):
      losses = []
      net_work.set_train()

      epoch_start = time.time()

      # Read in data for each training round
      for i, (images, labels) in enumerate(data_loader_train):
          labels = labels.astype(ms.int32)
          loss = train_step(images, labels)
          losses.append(loss)

      # Verify the accuracy after each epoch

      acc = model1.eval(dataset_val)['Accuracy']

      epoch_end = time.time()
      epoch_seconds = (epoch_end - epoch_start) * 1000
      step_seconds = epoch_seconds/step_size_train

      print("-" * 20)
      print("Epoch: [%3d/%3d], Average Train Loss: [%5.3f], Accuracy: [%5.3f]" % (
          epoch+1, num_epochs, sum(losses)/len(losses), acc
      ))
      print("epoch time: %5.3f ms, per step time: %5.3f ms" % (
          epoch_seconds, step_seconds
      ))

      if acc > best_acc:
          best_acc = acc
          if not os.path.exists(best_ckpt_dir):
              os.mkdir(best_ckpt_dir)
          ms.save_checkpoint(net_work, best_ckpt_path)

  print("=" * 80)
  print(f"End of validation the best Accuracy is: {best_acc: 5.3f}, "
        f"save the best ckpt file in {best_ckpt_path}", flush=True)

  visualize_model(best_ckpt_path, dataset_val)
  """
  print(rntl)

## 
def sentiment_analysis_rnn():
  sarnn  = """
  import os
  import shutil
  import requests
  import tempfile
  from tqdm import tqdm
  from typing import IO
  from pathlib import Path

  # Set the storage path to `home_path/.mindspore_examples`.
  cache_dir = Path.home() / '.mindspore_examples'

  def http_get(url: str, temp_file: IO):
      req = requests.get(url, stream=True)
      content_length = req.headers.get('Content-Length')
      total = int(content_length) if content_length is not None else None
      progress = tqdm(unit='B', total=total)
      for chunk in req.iter_content(chunk_size=1024):
          if chunk:
              progress.update(len(chunk))
              temp_file.write(chunk)
      progress.close()

  def download(file_name: str, url: str):
      if not os.path.exists(cache_dir):
          os.makedirs(cache_dir)
      cache_path = os.path.join(cache_dir, file_name)
      cache_exist = os.path.exists(cache_path)
      if not cache_exist:
          with tempfile.NamedTemporaryFile() as temp_file:
              http_get(url, temp_file)
              temp_file.flush()
              temp_file.seek(0)
              with open(cache_path, 'wb') as cache_file:
                  shutil.copyfileobj(temp_file, cache_file)
      return cache_path

  imdb_path = download('aclImdb_v1.tar.gz', 'https://mindspore-website.obs.myhuaweicloud.com/notebook/datasets/aclImdb_v1.tar.gz')
  imdb_path

  import re
  import six
  import string
  import tarfile

  class IMDBData():
      label_map = {
          "pos": 1,
          "neg": 0
      }
      def __init__(self, path, mode="train"):
          self.mode = mode
          self.path = path
          self.docs, self.labels = [], []

          self._load("pos")
          self._load("neg")

      def _load(self, label):
          pattern = re.compile(r"aclImdb/{}/{}/.*\.txt$".format(self.mode, label))
          # Load data to the memory.
          with tarfile.open(self.path) as tarf:
              tf = tarf.next()
              while tf is not None:
                  if bool(pattern.match(tf.name)):
                      # Segment text, remove punctuations and special characters, and convert text to lowercase.
                      self.docs.append(str(tarf.extractfile(tf).read().rstrip(six.b("\n\r"))
                                          .translate(None, six.b(string.punctuation)).lower()).split())
                      self.labels.append([self.label_map[label]])
                  tf = tarf.next()

      def __getitem__(self, idx):
          return self.docs[idx], self.labels[idx]

      def __len__(self):
          return len(self.docs)

  imdb_train = IMDBData(imdb_path, 'train')
  len(imdb_train)

  import mindspore.dataset as ds

  def load_imdb(imdb_path):
      imdb_train = ds.GeneratorDataset(IMDBData(imdb_path, "train"), column_names=["text", "label"], shuffle=True)
      imdb_test = ds.GeneratorDataset(IMDBData(imdb_path, "test"), column_names=["text", "label"], shuffle=False)
      return imdb_train, imdb_test

  imdb_train, imdb_test = load_imdb(imdb_path)
  imdb_train

  import zipfile
  import numpy as np

  def load_glove(glove_path):
      glove_100d_path = os.path.join(cache_dir, 'glove.6B.100d.txt')
      if not os.path.exists(glove_100d_path):
          glove_zip = zipfile.ZipFile(glove_path)
          glove_zip.extractall(cache_dir)

      embeddings = []
      tokens = []
      with open(glove_100d_path, encoding='utf-8') as gf:
          for glove in gf:
              word, embedding = glove.split(maxsplit=1)
              tokens.append(word)
              embeddings.append(np.fromstring(embedding, dtype=np.float32, sep=' '))
      # Add the embeddings corresponding to the special placeholders <unk> and <pad>.
      embeddings.append(np.random.rand(100))
      embeddings.append(np.zeros((100,), np.float32))

      vocab = ds.text.Vocab.from_list(tokens, special_tokens=["<unk>", "<pad>"], special_first=False)
      embeddings = np.array(embeddings).astype(np.float32)
      return vocab, embeddings

  glove_path = download('glove.6B.zip', 'https://mindspore-website.obs.myhuaweicloud.com/notebook/datasets/glove.6B.zip')
  vocab, embeddings = load_glove(glove_path)
  len(vocab.vocab())

  idx = vocab.tokens_to_ids('the')
  embedding = embeddings[idx]
  idx, embedding

  import mindspore as ms

  lookup_op = ds.text.Lookup(vocab, unknown_token='<unk>')
  pad_op = ds.transforms.PadEnd([500], pad_value=vocab.tokens_to_ids('<pad>'))
  type_cast_op = ds.transforms.TypeCast(ms.float32)

  imdb_train = imdb_train.map(operations=[lookup_op, pad_op], input_columns=['text'])
  imdb_train = imdb_train.map(operations=[type_cast_op], input_columns=['label'])

  imdb_test = imdb_test.map(operations=[lookup_op, pad_op], input_columns=['text'])
  imdb_test = imdb_test.map(operations=[type_cast_op], input_columns=['label'])

  imdb_train, imdb_valid = imdb_train.split([0.7, 0.3])

  imdb_train = imdb_train.batch(64, drop_remainder=True)
  imdb_valid = imdb_valid.batch(64, drop_remainder=True)

  import math
  import mindspore as ms
  import mindspore.nn as nn
  import mindspore.ops as ops
  from mindspore.common.initializer import Uniform, HeUniform

  class RNN(nn.Cell):
      def __init__(self, embeddings, hidden_dim, output_dim, n_layers,
                  bidirectional, pad_idx):
          super().__init__()
          vocab_size, embedding_dim = embeddings.shape
          self.embedding = nn.Embedding(vocab_size, embedding_dim, embedding_table=ms.Tensor(embeddings), padding_idx=pad_idx)
          self.rnn = nn.LSTM(embedding_dim,
                            hidden_dim,
                            num_layers=n_layers,
                            bidirectional=bidirectional,
                            batch_first=True)
          weight_init = HeUniform(math.sqrt(5))
          bias_init = Uniform(1 / math.sqrt(hidden_dim * 2))
          self.fc = nn.Dense(hidden_dim * 2, output_dim, weight_init=weight_init, bias_init=bias_init)

      def construct(self, inputs):
          embedded = self.embedding(inputs)
          _, (hidden, _) = self.rnn(embedded)
          hidden = ops.concat((hidden[-2, :, :], hidden[-1, :, :]), axis=1)
          output = self.fc(hidden)
          return output

  hidden_size = 256
  output_size = 1
  num_layers = 2
  bidirectional = True
  lr = 0.001
  pad_idx = vocab.tokens_to_ids('<pad>')

  model = RNN(embeddings, hidden_size, output_size, num_layers, bidirectional, pad_idx)
  loss_fn = nn.BCEWithLogitsLoss(reduction='mean')
  optimizer = nn.Adam(model.trainable_params(), learning_rate=lr)

  def forward_fn(data, label):
      logits = model(data)
      loss = loss_fn(logits, label)
      return loss

  grad_fn = ms.value_and_grad(forward_fn, None, optimizer.parameters)

  def train_step(data, label):
      loss, grads = grad_fn(data, label)
      optimizer(grads)
      return loss

  def train_one_epoch(model, train_dataset, epoch=0):
      model.set_train()
      total = train_dataset.get_dataset_size()
      loss_total = 0
      step_total = 0
      with tqdm(total=total) as t:
          t.set_description('Epoch %i' % epoch)
          for i in train_dataset.create_tuple_iterator():
              loss = train_step(*i)
              loss_total += loss.asnumpy()
              step_total += 1
              t.set_postfix(loss=loss_total/step_total)
              t.update(1)

  def binary_accuracy(preds, y):

      # Round off the predicted value.
      rounded_preds = np.around(ops.sigmoid(preds).asnumpy())
      correct = (rounded_preds == y).astype(np.float32)
      acc = correct.sum() / len(correct)
      return acc

  def evaluate(model, test_dataset, criterion, epoch=0):
      total = test_dataset.get_dataset_size()
      epoch_loss = 0
      epoch_acc = 0
      step_total = 0
      model.set_train(False)

      with tqdm(total=total) as t:
          t.set_description('Epoch %i' % epoch)
          for i in test_dataset.create_tuple_iterator():
              predictions = model(i[0])
              loss = criterion(predictions, i[1])
              epoch_loss += loss.asnumpy()

              acc = binary_accuracy(predictions, i[1])
              epoch_acc += acc

              step_total += 1
              t.set_postfix(loss=epoch_loss/step_total, acc=epoch_acc/step_total)
              t.update(1)

      return epoch_loss / total

  num_epochs = 5
  best_valid_loss = float('inf')
  ckpt_file_name = os.path.join(cache_dir, 'sentiment-analysis.ckpt')

  for epoch in range(num_epochs):
      train_one_epoch(model, imdb_train, epoch)
      valid_loss = evaluate(model, imdb_valid, loss_fn, epoch)

      if valid_loss < best_valid_loss:
          best_valid_loss = valid_loss
          ms.save_checkpoint(model, ckpt_file_name)

  param_dict = ms.load_checkpoint(ckpt_file_name)
  ms.load_param_into_net(model, param_dict)

  imdb_test = imdb_test.batch(64)
  evaluate(model, imdb_test, loss_fn)

  score_map = {
      1: "Positive",
      0: "Negative"
  }

  def predict_sentiment(model, vocab, sentence):
      model.set_train(False)
      tokenized = sentence.lower().split()
      indexed = vocab.tokens_to_ids(tokenized)
      tensor = ms.Tensor(indexed, ms.int32)
      tensor = tensor.expand_dims(0)
      prediction = model(tensor)
      return score_map[int(np.round(ops.sigmoid(prediction).asnumpy()))]

  predict_sentiment(model, vocab, "This film is terrible")

  predict_sentiment(model, vocab, "This film is great")
  """
  print(sarnn)