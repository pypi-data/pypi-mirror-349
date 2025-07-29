def cyclegan():
  cg = """
  ###############################################################################################################
  # CODE BLOCK 1
  ###############################################################################################################
  from download import download

  url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/models/application/CycleGAN_apple2orange.zip"

  download(url, ".", kind="zip", replace=True)

  ###############################################################################################################
  # CODE BLOCK 2
  ###############################################################################################################
  from mindspore.dataset import MindDataset

  # Read data in MindRecord format.
  name_mr = "./CycleGAN_apple2orange/apple2orange_train.mindrecord"
  data = MindDataset(dataset_files=name_mr)
  print("Datasize: ", data.get_dataset_size())

  batch_size = 1
  dataset = data.batch(batch_size)
  datasize = dataset.get_dataset_size()

  ###############################################################################################################
  # CODE BLOCK 1
  ###############################################################################################################

  import numpy as np
  import matplotlib.pyplot as plt

  mean = 0.5 * 255
  std = 0.5 * 255

  plt.figure(figsize=(12, 5), dpi=60)
  for i, data in enumerate(dataset.create_dict_iterator()):
      if i < 5:
          show_images_a = data["image_A"].asnumpy()
          show_images_b = data["image_B"].asnumpy()

          plt.subplot(2, 5, i+1)
          show_images_a = (show_images_a[0] * std + mean).astype(np.uint8).transpose((1, 2, 0))
          plt.imshow(show_images_a)
          plt.axis("off")

          plt.subplot(2, 5, i+6)
          show_images_b = (show_images_b[0] * std + mean).astype(np.uint8).transpose((1, 2, 0))
          plt.imshow(show_images_b)
          plt.axis("off")
      else:
          break
  plt.show()
  ###############################################################################################################
  # CODE BLOCK 3
  ###############################################################################################################
  import mindspore.nn as nn
  import mindspore.ops as ops
  from mindspore.common.initializer import Normal

  weight_init = Normal(sigma=0.02)

  class ConvNormReLU(nn.Cell):
      def __init__(self, input_channel, out_planes, kernel_size=4, stride=2, alpha=0.2, norm_mode='instance',
                  pad_mode='CONSTANT', use_relu=True, padding=None, transpose=False):
          super(ConvNormReLU, self).__init__()
          norm = nn.BatchNorm2d(out_planes)
          if norm_mode == 'instance':
              norm = nn.BatchNorm2d(out_planes, affine=False)
          has_bias = (norm_mode == 'instance')
          if padding is None:
              padding = (kernel_size - 1) // 2
          if pad_mode == 'CONSTANT':
              if transpose:
                  conv = nn.Conv2dTranspose(input_channel, out_planes, kernel_size, stride, pad_mode='same',
                                            has_bias=has_bias, weight_init=weight_init)
              else:
                  conv = nn.Conv2d(input_channel, out_planes, kernel_size, stride, pad_mode='pad',
                                  has_bias=has_bias, padding=padding, weight_init=weight_init)
              layers = [conv, norm]
          else:
              paddings = ((0, 0), (0, 0), (padding, padding), (padding, padding))
              pad = nn.Pad(paddings=paddings, mode=pad_mode)
              if transpose:
                  conv = nn.Conv2dTranspose(input_channel, out_planes, kernel_size, stride, pad_mode='pad',
                                            has_bias=has_bias, weight_init=weight_init)
              else:
                  conv = nn.Conv2d(input_channel, out_planes, kernel_size, stride, pad_mode='pad',
                                  has_bias=has_bias, weight_init=weight_init)
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


  class ResidualBlock(nn.Cell):
      def __init__(self, dim, norm_mode='instance', dropout=False, pad_mode="CONSTANT"):
          super(ResidualBlock, self).__init__()
          self.conv1 = ConvNormReLU(dim, dim, 3, 1, 0, norm_mode, pad_mode)
          self.conv2 = ConvNormReLU(dim, dim, 3, 1, 0, norm_mode, pad_mode, use_relu=False)
          self.dropout = dropout
          if dropout:
              self.dropout = nn.Dropout(p=0.5)

      def construct(self, x):
          out = self.conv1(x)
          if self.dropout:
              out = self.dropout(out)
          out = self.conv2(out)
          return x + out


  class ResNetGenerator(nn.Cell):
      def __init__(self, input_channel=3, output_channel=64, n_layers=9, alpha=0.2, norm_mode='instance', dropout=False,
                  pad_mode="CONSTANT"):
          super(ResNetGenerator, self).__init__()
          self.conv_in = ConvNormReLU(input_channel, output_channel, 7, 1, alpha, norm_mode, pad_mode=pad_mode)
          self.down_1 = ConvNormReLU(output_channel, output_channel * 2, 3, 2, alpha, norm_mode)
          self.down_2 = ConvNormReLU(output_channel * 2, output_channel * 4, 3, 2, alpha, norm_mode)
          layers = [ResidualBlock(output_channel * 4, norm_mode, dropout=dropout, pad_mode=pad_mode)] * n_layers
          self.residuals = nn.SequentialCell(layers)
          self.up_2 = ConvNormReLU(output_channel * 4, output_channel * 2, 3, 2, alpha, norm_mode, transpose=True)
          self.up_1 = ConvNormReLU(output_channel * 2, output_channel, 3, 2, alpha, norm_mode, transpose=True)
          if pad_mode == "CONSTANT":
              self.conv_out = nn.Conv2d(output_channel, 3, kernel_size=7, stride=1, pad_mode='pad',
                                        padding=3, weight_init=weight_init)
          else:
              pad = nn.Pad(paddings=((0, 0), (0, 0), (3, 3), (3, 3)), mode=pad_mode)
              conv = nn.Conv2d(output_channel, 3, kernel_size=7, stride=1, pad_mode='pad', weight_init=weight_init)
              self.conv_out = nn.SequentialCell([pad, conv])

      def construct(self, x):
          x = self.conv_in(x)
          x = self.down_1(x)
          x = self.down_2(x)
          x = self.residuals(x)
          x = self.up_2(x)
          x = self.up_1(x)
          output = self.conv_out(x)
          return ops.tanh(output)

  # Instantiate the generator.
  net_rg_a = ResNetGenerator()
  net_rg_a.update_parameters_name('net_rg_a.')

  net_rg_b = ResNetGenerator()
  net_rg_b.update_parameters_name('net_rg_b.')

  ###############################################################################################################
  # CODE BLOCK 4
  ###############################################################################################################
  # Define a discriminator.
  class Discriminator(nn.Cell):
      def __init__(self, input_channel=3, output_channel=64, n_layers=3, alpha=0.2, norm_mode='instance'):
          super(Discriminator, self).__init__()
          kernel_size = 4
          layers = [nn.Conv2d(input_channel, output_channel, kernel_size, 2, pad_mode='pad', padding=1, weight_init=weight_init),
                    nn.LeakyReLU(alpha)]
          nf_mult = output_channel
          for i in range(1, n_layers):
              nf_mult_prev = nf_mult
              nf_mult = min(2 ** i, 8) * output_channel
              layers.append(ConvNormReLU(nf_mult_prev, nf_mult, kernel_size, 2, alpha, norm_mode, padding=1))
          nf_mult_prev = nf_mult
          nf_mult = min(2 ** n_layers, 8) * output_channel
          layers.append(ConvNormReLU(nf_mult_prev, nf_mult, kernel_size, 1, alpha, norm_mode, padding=1))
          layers.append(nn.Conv2d(nf_mult, 1, kernel_size, 1, pad_mode='pad', padding=1, weight_init=weight_init))
          self.features = nn.SequentialCell(layers)

      def construct(self, x):
          output = self.features(x)
          return output

  # Initialize the discriminator.
  net_d_a = Discriminator()
  net_d_a.update_parameters_name('net_d_a.')

  net_d_b = Discriminator()
  net_d_b.update_parameters_name('net_d_b.')

  ###############################################################################################################
  # CODE BLOCK 5
  ###############################################################################################################
  # Build a generator, discriminator, and optimizer.
  optimizer_rg_a = nn.Adam(net_rg_a.trainable_params(), learning_rate=0.0002, beta1=0.5)
  optimizer_rg_b = nn.Adam(net_rg_b.trainable_params(), learning_rate=0.0002, beta1=0.5)

  optimizer_d_a = nn.Adam(net_d_a.trainable_params(), learning_rate=0.0002, beta1=0.5)
  optimizer_d_b = nn.Adam(net_d_b.trainable_params(), learning_rate=0.0002, beta1=0.5)

  # GAN loss function. The sigmoid function is not used at the last layer.
  loss_fn = nn.MSELoss(reduction='mean')
  l1_loss = nn.L1Loss("mean")

  def gan_loss(predict, target):
      target = ops.ones_like(predict) * target
      loss = loss_fn(predict, target)
      return loss

  ###############################################################################################################
  # CODE BLOCK 6
  ###############################################################################################################

  import mindspore as ms

  # Forward computation

  def generator(img_a, img_b):
      fake_a = net_rg_b(img_b)
      fake_b = net_rg_a(img_a)
      rec_a = net_rg_b(fake_b)
      rec_b = net_rg_a(fake_a)
      identity_a = net_rg_b(img_a)
      identity_b = net_rg_a(img_b)
      return fake_a, fake_b, rec_a, rec_b, identity_a, identity_b

  lambda_a = 10.0
  lambda_b = 10.0
  lambda_idt = 0.5

  def generator_forward(img_a, img_b):
      true = Tensor(True, dtype.bool_)
      fake_a, fake_b, rec_a, rec_b, identity_a, identity_b = generator(img_a, img_b)
      loss_g_a = gan_loss(net_d_b(fake_b), true)
      loss_g_b = gan_loss(net_d_a(fake_a), true)
      loss_c_a = l1_loss(rec_a, img_a) * lambda_a
      loss_c_b = l1_loss(rec_b, img_b) * lambda_b
      loss_idt_a = l1_loss(identity_a, img_a) * lambda_a * lambda_idt
      loss_idt_b = l1_loss(identity_b, img_b) * lambda_b * lambda_idt
      loss_g = loss_g_a + loss_g_b + loss_c_a + loss_c_b + loss_idt_a + loss_idt_b
      return fake_a, fake_b, loss_g, loss_g_a, loss_g_b, loss_c_a, loss_c_b, loss_idt_a, loss_idt_b

  def generator_forward_grad(img_a, img_b):
      _, _, loss_g, _, _, _, _, _, _ = generator_forward(img_a, img_b)
      return loss_g

  def discriminator_forward(img_a, img_b, fake_a, fake_b):
      false = Tensor(False, dtype.bool_)
      true = Tensor(True, dtype.bool_)
      d_fake_a = net_d_a(fake_a)
      d_img_a = net_d_a(img_a)
      d_fake_b = net_d_b(fake_b)
      d_img_b = net_d_b(img_b)
      loss_d_a = gan_loss(d_fake_a, false) + gan_loss(d_img_a, true)
      loss_d_b = gan_loss(d_fake_b, false) + gan_loss(d_img_b, true)
      loss_d = (loss_d_a + loss_d_b) * 0.5
      return loss_d

  def discriminator_forward_a(img_a, fake_a):
      false = Tensor(False, dtype.bool_)
      true = Tensor(True, dtype.bool_)
      d_fake_a = net_d_a(fake_a)
      d_img_a = net_d_a(img_a)
      loss_d_a = gan_loss(d_fake_a, false) + gan_loss(d_img_a, true)
      return loss_d_a

  def discriminator_forward_b(img_b, fake_b):
      false = Tensor(False, dtype.bool_)
      true = Tensor(True, dtype.bool_)
      d_fake_b = net_d_b(fake_b)
      d_img_b = net_d_b(img_b)
      loss_d_b = gan_loss(d_fake_b, false) + gan_loss(d_img_b, true)
      return loss_d_b

  # An image buffer is reserved to store the 50 images created previously.
  pool_size = 50
  def image_pool(images):
      num_imgs = 0
      image1 = []
      if isinstance(images, Tensor):
          images = images.asnumpy()
      return_images = []
      for image in images:
          if num_imgs < pool_size:
              num_imgs = num_imgs + 1
              image1.append(image)
              return_images.append(image)
          else:
              if random.uniform(0, 1) > 0.5:
                  random_id = random.randint(0, pool_size - 1)

                  tmp = image1[random_id].copy()
                  image1[random_id] = image
                  return_images.append(tmp)

              else:
                  return_images.append(image)
      output = Tensor(return_images, ms.float32)
      if output.ndim != 4:
          raise ValueError("img should be 4d, but get shape {}".format(output.shape))
      return output

  ###############################################################################################################
  # CODE BLOCK 6
  ###############################################################################################################
  from mindspore import value_and_grad

  # Instantiate the gradient calculation method.
  grad_g_a = value_and_grad(generator_forward_grad, None, net_rg_a.trainable_params())
  grad_g_b = value_and_grad(generator_forward_grad, None, net_rg_b.trainable_params())

  grad_d_a = value_and_grad(discriminator_forward_a, None, net_d_a.trainable_params())
  grad_d_b = value_and_grad(discriminator_forward_b, None, net_d_b.trainable_params())

  # Calculate the gradient of the generator and backpropagate the update parameters.
  def train_step_g(img_a, img_b):
      net_d_a.set_grad(False)
      net_d_b.set_grad(False)

      fake_a, fake_b, lg, lga, lgb, lca, lcb, lia, lib = generator_forward(img_a, img_b)

      _, grads_g_a = grad_g_a(img_a, img_b)
      _, grads_g_b = grad_g_b(img_a, img_b)
      optimizer_rg_a(grads_g_a)
      optimizer_rg_b(grads_g_b)

      return fake_a, fake_b, lg, lga, lgb, lca, lcb, lia, lib

  # Calculate the gradient of the discriminator and backpropagate the update parameters.
  def train_step_d(img_a, img_b, fake_a, fake_b):
      net_d_a.set_grad(True)
      net_d_b.set_grad(True)

      loss_d_a, grads_d_a = grad_d_a(img_a, fake_a)
      loss_d_b, grads_d_b = grad_d_b(img_b, fake_b)

      loss_d = (loss_d_a + loss_d_b) * 0.5

      optimizer_d_a(grads_d_a)
      optimizer_d_b(grads_d_b)

      return loss_d

  ###############################################################################################################
  # CODE BLOCK 6
  ###############################################################################################################

  import os
  import time
  import random
  import numpy as np
  from PIL import Image
  from mindspore import Tensor, save_checkpoint
  from mindspore import dtype

  epochs = 7
  save_step_num = 80
  save_checkpoint_epochs = 1
  save_ckpt_dir = './train_ckpt_outputs/'

  print('Start training!')

  iterator = dataset.create_dict_iterator(num_epochs=epochs)
  for epoch in range(epochs):
      g_loss = []
      d_loss = []
      start_time_e = time.time()
      for step, data in enumerate(iterator):
          start_time_s = time.time()
          img_a = data["image_A"]
          img_b = data["image_B"]
          res_g = train_step_g(img_a, img_b)
          fake_a = res_g[0]
          fake_b = res_g[1]

          res_d = train_step_d(img_a, img_b, image_pool(fake_a), image_pool(fake_b))
          loss_d = float(res_d.asnumpy())
          step_time = time.time() - start_time_s

          res = []
          for item in res_g[2:]:
              res.append(float(item.asnumpy()))
          g_loss.append(res[0])
          d_loss.append(loss_d)

          if step % save_step_num == 0:
              print(f"Epoch:[{int(epoch + 1):>3d}/{int(epochs):>3d}], "
                    f"step:[{int(step):>4d}/{int(datasize):>4d}], "
                    f"time:{step_time:>3f}s,\n"
                    f"loss_g:{res[0]:.2f}, loss_d:{loss_d:.2f}, "
                    f"loss_g_a: {res[1]:.2f}, loss_g_b: {res[2]:.2f}, "
                    f"loss_c_a: {res[3]:.2f}, loss_c_b: {res[4]:.2f}, "
                    f"loss_idt_a: {res[5]:.2f}, loss_idt_b: {res[6]:.2f}")

      epoch_cost = time.time() - start_time_e
      per_step_time = epoch_cost / datasize
      mean_loss_d, mean_loss_g = sum(d_loss) / datasize, sum(g_loss) / datasize

      print(f"Epoch:[{int(epoch + 1):>3d}/{int(epochs):>3d}], "
            f"epoch time:{epoch_cost:.2f}s, per step time:{per_step_time:.2f}, "
            f"mean_g_loss:{mean_loss_g:.2f}, mean_d_loss:{mean_loss_d :.2f}")

      if epoch % save_checkpoint_epochs == 0:
          os.makedirs(save_ckpt_dir, exist_ok=True)
          save_checkpoint(net_rg_a, os.path.join(save_ckpt_dir, f"g_a_{epoch}.ckpt"))
          save_checkpoint(net_rg_b, os.path.join(save_ckpt_dir, f"g_b_{epoch}.ckpt"))
          save_checkpoint(net_d_a, os.path.join(save_ckpt_dir, f"d_a_{epoch}.ckpt"))
          save_checkpoint(net_d_b, os.path.join(save_ckpt_dir, f"d_b_{epoch}.ckpt"))

  print('End of training!')

  ###############################################################################################################
  # CODE BLOCK 6
  ###############################################################################################################
  import os
  from PIL import Image
  import mindspore.dataset as ds
  import mindspore.dataset.vision as vision
  from mindspore import load_checkpoint, load_param_into_net

  # Load the weight file.
  def load_ckpt(net, ckpt_dir):
      param_GA = load_checkpoint(ckpt_dir)
      load_param_into_net(net, param_GA)

  g_a_ckpt = './CycleGAN_apple2orange/ckpt/g_a.ckpt'
  g_b_ckpt = './CycleGAN_apple2orange/ckpt/g_b.ckpt'

  load_ckpt(net_rg_a, g_a_ckpt)
  load_ckpt(net_rg_b, g_b_ckpt)

  # Image inference
  fig = plt.figure(figsize=(11, 2.5), dpi=100)
  def eval_data(dir_path, net, a):

      def read_img():
          for dir in os.listdir(dir_path):
              path = os.path.join(dir_path, dir)
              img = Image.open(path).convert('RGB')
              yield img, dir

      dataset = ds.GeneratorDataset(read_img, column_names=["image", "image_name"])
      trans = [vision.Resize((256, 256)), vision.Normalize(mean=[0.5 * 255] * 3, std=[0.5 * 255] * 3), vision.HWC2CHW()]
      dataset = dataset.map(operations=trans, input_columns=["image"])
      dataset = dataset.batch(1)
      for i, data in enumerate(dataset.create_dict_iterator()):
          img = data["image"]
          fake = net(img)
          fake = (fake[0] * 0.5 * 255 + 0.5 * 255).astype(np.uint8).transpose((1, 2, 0))
          img = (img[0] * 0.5 * 255 + 0.5 * 255).astype(np.uint8).transpose((1, 2, 0))

          fig.add_subplot(2, 8, i+1+a)
          plt.axis("off")
          plt.imshow(img.asnumpy())

          fig.add_subplot(2, 8, i+9+a)
          plt.axis("off")
          plt.imshow(fake.asnumpy())

  eval_data('./CycleGAN_apple2orange/predict/apple', net_rg_a, 0)
  eval_data('./CycleGAN_apple2orange/predict/orange', net_rg_b, 4)
  plt.show()
  """
  print(cg)

## Diffusion Model
def diffusion_model():
  dfm = """
  import math
  from functools import partial
  # %matplotlib inline
  import matplotlib.pyplot as plt
  from tqdm.auto import tqdm
  import numpy as np
  from multiprocessing import cpu_count
  from download import download

  import mindspore as ms
  import mindspore.nn as nn
  import mindspore.ops as ops
  from mindspore import Tensor, Parameter
  from mindspore import dtype as mstype
  from mindspore.dataset.vision import Resize, Inter, CenterCrop, ToTensor, RandomHorizontalFlip, ToPIL
  from mindspore.common.initializer import initializer
  from mindspore.amp import DynamicLossScaler

  ms.set_seed(0)

  def rearrange(head, inputs):
      b, hc, x, y = inputs.shape
      c = hc // head
      return inputs.reshape((b, head, c, x * y))

  def rsqrt(x):
      res = ops.sqrt(x)
      return ops.inv(res)

  def randn_like(x, dtype=None):
      if dtype is None:
          dtype = x.dtype
      res = ops.standard_normal(x.shape).astype(dtype)
      return res

  def randn(shape, dtype=None):
      if dtype is None:
          dtype = ms.float32
      res = ops.standard_normal(shape).astype(dtype)
      return res

  def randint(low, high, size, dtype=ms.int32):
      res = ops.uniform(size, Tensor(low, dtype), Tensor(high, dtype), dtype=dtype)
      return res

  def exists(x):
      return x is not None

  def default(val, d):
      if exists(val):
          return val
      return d() if callable(d) else d

  def _check_dtype(d1, d2):
      if ms.float32 in (d1, d2):
          return ms.float32
      if d1 == d2:
          return d1
      raise ValueError('dtype is not supported.')

  class Residual(nn.Cell):
      def __init__(self, fn):
          super().__init__()
          self.fn = fn

      def construct(self, x, *args, **kwargs):
          return self.fn(x, *args, **kwargs) + x

  def Upsample(dim):
      return nn.Conv2dTranspose(dim, dim, 4, 2, pad_mode="pad", padding=1)

  def Downsample(dim):
      return nn.Conv2d(dim, dim, 4, 2, pad_mode="pad", padding=1)

  class SinusoidalPositionEmbeddings(nn.Cell):
      def __init__(self, dim):
          super().__init__()
          self.dim = dim
          half_dim = self.dim // 2
          emb = math.log(10000) / (half_dim - 1)
          emb = np.exp(np.arange(half_dim) * - emb)
          self.emb = Tensor(emb, ms.float32)

      def construct(self, x):
          emb = x[:, None] * self.emb[None, :]
          emb = ops.concat((ops.sin(emb), ops.cos(emb)), axis=-1)
          return emb

  class Block(nn.Cell):
      def __init__(self, dim, dim_out, groups=1):
          super().__init__()
          self.proj = nn.Conv2d(dim, dim_out, 3, pad_mode="pad", padding=1)
          self.proj = c(dim, dim_out, 3, padding=1, pad_mode='pad')
          self.norm = nn.GroupNorm(groups, dim_out)
          self.act = nn.SiLU()

      def construct(self, x, scale_shift=None):
          x = self.proj(x)
          x = self.norm(x)

          if exists(scale_shift):
              scale, shift = scale_shift
              x = x * (scale + 1) + shift

          x = self.act(x)
          return x

  class ConvNextBlock(nn.Cell):
      def __init__(self, dim, dim_out, *, time_emb_dim=None, mult=2, norm=True):
          super().__init__()
          self.mlp = (
              nn.SequentialCell(nn.GELU(), nn.Dense(time_emb_dim, dim))
              if exists(time_emb_dim)
              else None
          )

          self.ds_conv = nn.Conv2d(dim, dim, 7, padding=3, group=dim, pad_mode="pad")
          self.net = nn.SequentialCell(
              nn.GroupNorm(1, dim) if norm else nn.Identity(),
              nn.Conv2d(dim, dim_out * mult, 3, padding=1, pad_mode="pad"),
              nn.GELU(),
              nn.GroupNorm(1, dim_out * mult),
              nn.Conv2d(dim_out * mult, dim_out, 3, padding=1, pad_mode="pad"),
          )

          self.res_conv = nn.Conv2d(dim, dim_out, 1) if dim != dim_out else nn.Identity()

      def construct(self, x, time_emb=None):
          h = self.ds_conv(x)
          if exists(self.mlp) and exists(time_emb):
              assert exists(time_emb), "time embedding must be passed in"
              condition = self.mlp(time_emb)
              condition = condition.expand_dims(-1).expand_dims(-1)
              h = h + condition

          h = self.net(h)
          return h + self.res_conv(x)

  class Attention(nn.Cell):
      def __init__(self, dim, heads=4, dim_head=32):
          super().__init__()
          self.scale = dim_head ** -0.5
          self.heads = heads
          hidden_dim = dim_head * heads

          self.to_qkv = nn.Conv2d(dim, hidden_dim * 3, 1, pad_mode='valid', has_bias=False)
          self.to_out = nn.Conv2d(hidden_dim, dim, 1, pad_mode='valid', has_bias=True)
          self.map = ops.Map()
          self.partial = ops.Partial()

      def construct(self, x):
          b, _, h, w = x.shape
          qkv = self.to_qkv(x).chunk(3, 1)
          q, k, v = self.map(self.partial(rearrange, self.heads), qkv)

          q = q * self.scale

          # 'b h d i, b h d j -> b h i j'
          sim = ops.bmm(q.swapaxes(2, 3), k)
          attn = ops.softmax(sim, axis=-1)
          # 'b h i j, b h d j -> b h i d'
          out = ops.bmm(attn, v.swapaxes(2, 3))
          out = out.swapaxes(-1, -2).reshape((b, -1, h, w))

          return self.to_out(out)


  class LayerNorm(nn.Cell):
      def __init__(self, dim):
          super().__init__()
          self.g = Parameter(initializer('ones', (1, dim, 1, 1)), name='g')

      def construct(self, x):
          eps = 1e-5
          var = x.var(1, keepdims=True)
          mean = x.mean(1, keep_dims=True)
          return (x - mean) * rsqrt((var + eps)) * self.g


  class LinearAttention(nn.Cell):
      def __init__(self, dim, heads=4, dim_head=32):
          super().__init__()
          self.scale = dim_head ** -0.5
          self.heads = heads
          hidden_dim = dim_head * heads
          self.to_qkv = nn.Conv2d(dim, hidden_dim * 3, 1, pad_mode='valid', has_bias=False)

          self.to_out = nn.SequentialCell(
              nn.Conv2d(hidden_dim, dim, 1, pad_mode='valid', has_bias=True),
              LayerNorm(dim)
          )

          self.map = ops.Map()
          self.partial = ops.Partial()

      def construct(self, x):
          b, _, h, w = x.shape
          qkv = self.to_qkv(x).chunk(3, 1)
          q, k, v = self.map(self.partial(rearrange, self.heads), qkv)

          q = ops.softmax(q, -2)
          k = ops.softmax(k, -1)

          q = q * self.scale
          v = v / (h * w)

          # 'b h d n, b h e n -> b h d e'
          context = ops.bmm(k, v.swapaxes(2, 3))
          # 'b h d e, b h d n -> b h e n'
          out = ops.bmm(context.swapaxes(2, 3), q)

          out = out.reshape((b, -1, h, w))
          return self.to_out(out)

  class PreNorm(nn.Cell):
      def __init__(self, dim, fn):
          super().__init__()
          self.fn = fn
          self.norm = nn.GroupNorm(1, dim)

      def construct(self, x):
          x = self.norm(x)
          return self.fn(x)

  class Unet(nn.Cell):
      def __init__(
              self,
              dim,
              init_dim=None,
              out_dim=None,
              dim_mults=(1, 2, 4, 8),
              channels=3,
              with_time_emb=True,
              convnext_mult=2,
      ):
          super().__init__()

          self.channels = channels

          init_dim = default(init_dim, dim // 3 * 2)
          self.init_conv = nn.Conv2d(channels, init_dim, 7, padding=3, pad_mode="pad", has_bias=True)

          dims = [init_dim, *map(lambda m: dim * m, dim_mults)]
          in_out = list(zip(dims[:-1], dims[1:]))

          block_klass = partial(ConvNextBlock, mult=convnext_mult)

          if with_time_emb:
              time_dim = dim * 4
              self.time_mlp = nn.SequentialCell(
                  SinusoidalPositionEmbeddings(dim),
                  nn.Dense(dim, time_dim),
                  nn.GELU(),
                  nn.Dense(time_dim, time_dim),
              )
          else:
              time_dim = None
              self.time_mlp = None

          self.downs = nn.CellList([])
          self.ups = nn.CellList([])
          num_resolutions = len(in_out)

          for ind, (dim_in, dim_out) in enumerate(in_out):
              is_last = ind >= (num_resolutions - 1)

              self.downs.append(
                  nn.CellList(
                      [
                          block_klass(dim_in, dim_out, time_emb_dim=time_dim),
                          block_klass(dim_out, dim_out, time_emb_dim=time_dim),
                          Residual(PreNorm(dim_out, LinearAttention(dim_out))),
                          Downsample(dim_out) if not is_last else nn.Identity(),
                      ]
                  )
              )

          mid_dim = dims[-1]
          self.mid_block1 = block_klass(mid_dim, mid_dim, time_emb_dim=time_dim)
          self.mid_attn = Residual(PreNorm(mid_dim, Attention(mid_dim)))
          self.mid_block2 = block_klass(mid_dim, mid_dim, time_emb_dim=time_dim)

          for ind, (dim_in, dim_out) in enumerate(reversed(in_out[1:])):
              is_last = ind >= (num_resolutions - 1)

              self.ups.append(
                  nn.CellList(
                      [
                          block_klass(dim_out * 2, dim_in, time_emb_dim=time_dim),
                          block_klass(dim_in, dim_in, time_emb_dim=time_dim),
                          Residual(PreNorm(dim_in, LinearAttention(dim_in))),
                          Upsample(dim_in) if not is_last else nn.Identity(),
                      ]
                  )
              )

          out_dim = default(out_dim, channels)
          self.final_conv = nn.SequentialCell(
              block_klass(dim, dim), nn.Conv2d(dim, out_dim, 1)
          )

      def construct(self, x, time):
          x = self.init_conv(x)

          t = self.time_mlp(time) if exists(self.time_mlp) else None

          h = []

          for block1, block2, attn, downsample in self.downs:
              x = block1(x, t)
              x = block2(x, t)
              x = attn(x)
              h.append(x)

              x = downsample(x)

          x = self.mid_block1(x, t)
          x = self.mid_attn(x)
          x = self.mid_block2(x, t)

          len_h = len(h) - 1
          for block1, block2, attn, upsample in self.ups:
              x = ops.concat((x, h[len_h]), 1)
              len_h -= 1
              x = block1(x, t)
              x = block2(x, t)
              x = attn(x)

              x = upsample(x)
          return self.final_conv(x)

  def linear_beta_schedule(timesteps):
      beta_start = 0.0001
      beta_end = 0.02
      return np.linspace(beta_start, beta_end, timesteps).astype(np.float32)

  # Set the time steps to 200.
  timesteps = 200

  # Define a beta schedule.
  betas = linear_beta_schedule(timesteps=timesteps)

  # Define alphas.
  alphas = 1. - betas
  alphas_cumprod = np.cumprod(alphas, axis=0)
  alphas_cumprod_prev = np.pad(alphas_cumprod[:-1], (1, 0), constant_values=1)

  sqrt_recip_alphas = Tensor(np.sqrt(1. / alphas))
  sqrt_alphas_cumprod = Tensor(np.sqrt(alphas_cumprod))
  sqrt_one_minus_alphas_cumprod = Tensor(np.sqrt(1. - alphas_cumprod))

  # Calculate q(x_{t-1} | x_t, x_0).
  posterior_variance = betas * (1. - alphas_cumprod_prev) / (1. - alphas_cumprod)

  p2_loss_weight = (1 + alphas_cumprod / (1 - alphas_cumprod)) ** -0.
  p2_loss_weight = Tensor(p2_loss_weight)

  def extract(a, t, x_shape):
      b = t.shape[0]
      out = Tensor(a).gather(t, -1)
      return out.reshape(b, *((1,) * (len(x_shape) - 1)))

  # Download the cat image.
  url = 'https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/image_cat.zip'
  path = download(url, './', kind="zip", replace=True)

  from PIL import Image

  image = Image.open('./image_cat/jpg/000000039769.jpg')
  base_width = 160
  image = image.resize((base_width, int(float(image.size[1]) * float(base_width / float(image.size[0])))))
  image.show()

  from mindspore.dataset import ImageFolderDataset

  image_size = 128
  transforms = [
      Resize(image_size, Inter.BILINEAR),
      CenterCrop(image_size),
      ToTensor(),
      lambda t: (t * 2) - 1
  ]


  path = './image_cat'
  dataset = ImageFolderDataset(dataset_dir=path, num_parallel_workers=cpu_count(),
                              extensions=['.jpg', '.jpeg', '.png', '.tiff'],
                              num_shards=1, shard_id=0, shuffle=False, decode=True)
  dataset = dataset.project('image')
  transforms.insert(1, RandomHorizontalFlip())
  dataset_1 = dataset.map(transforms, 'image')
  dataset_2 = dataset_1.batch(1, drop_remainder=True)
  x_start = next(dataset_2.create_tuple_iterator())[0]
  print(x_start.shape)

  import numpy as np

  reverse_transform = [
      lambda t: (t + 1) / 2,
      lambda t: ops.permute(t, (1, 2, 0)), # CHW to HWC
      lambda t: t * 255.,
      lambda t: t.asnumpy().astype(np.uint8),
      ToPIL()
  ]

  def compose(transform, x):
      for d in transform:
          x = d(x)
      return x

  reverse_image = compose(reverse_transform, x_start[0])
  reverse_image.show()

  def q_sample(x_start, t, noise=None):
      if noise is None:
          noise = randn_like(x_start)
      return (extract(sqrt_alphas_cumprod, t, x_start.shape) * x_start +
              extract(sqrt_one_minus_alphas_cumprod, t, x_start.shape) * noise)

  def get_noisy_image(x_start, t):
      # Add noise.
      x_noisy = q_sample(x_start, t=t)

      # Transform to a PIL image.
      noisy_image = compose(reverse_transform, x_noisy[0])

      return noisy_image

  # Sets the time step.
  t = Tensor([40])
  noisy_image = get_noisy_image(x_start, t)
  print(noisy_image)
  noisy_image.show()

  import matplotlib.pyplot as plt

  def plot(imgs, with_orig=False, row_title=None, **imshow_kwargs):
      if not isinstance(imgs[0], list):
          imgs = [imgs]

      num_rows = len(imgs)
      num_cols = len(imgs[0]) + with_orig
      _, axs = plt.subplots(figsize=(200, 200), nrows=num_rows, ncols=num_cols, squeeze=False)
      for row_idx, row in enumerate(imgs):
          row = [image] + row if with_orig else row
          for col_idx, img in enumerate(row):
              ax = axs[row_idx, col_idx]
              ax.imshow(np.asarray(img), **imshow_kwargs)
              ax.set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

      if with_orig:
          axs[0, 0].set(title='Original image')
          axs[0, 0].title.set_size(8)
      if row_title is not None:
          for row_idx in range(num_rows):
              axs[row_idx, 0].set(ylabel=row_title[row_idx])

      plt.tight_layout()

  plot([get_noisy_image(x_start, Tensor([t])) for t in [0, 50, 100, 150, 199]])

  def p_losses(unet_model, x_start, t, noise=None):
      if noise is None:
          noise = randn_like(x_start)
      x_noisy = q_sample(x_start=x_start, t=t, noise=noise)
      predicted_noise = unet_model(x_noisy, t)

      loss = nn.SmoothL1Loss()(noise, predicted_noise)# todo
      loss = loss.reshape(loss.shape[0], -1)
      loss = loss * extract(p2_loss_weight, t, loss.shape)
      return loss.mean()

  # Download the MNIST dataset.
  url = 'https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/dataset.zip'
  path = download(url, './', kind="zip", replace=True)

  from mindspore.dataset import FashionMnistDataset

  image_size = 28
  channels = 1
  batch_size = 16

  fashion_mnist_dataset_dir = "./dataset"
  dataset = FashionMnistDataset(dataset_dir=fashion_mnist_dataset_dir, usage="train", num_parallel_workers=cpu_count(), shuffle=True, num_shards=1, shard_id=0)

  transforms = [
      RandomHorizontalFlip(),
      ToTensor(),
      lambda t: (t * 2) - 1
  ]


  dataset = dataset.project('image')
  dataset = dataset.shuffle(64)
  dataset = dataset.map(transforms, 'image')
  dataset = dataset.batch(16, drop_remainder=True)

  x = next(dataset.create_dict_iterator())
  print(x.keys())

  dict_keys(['image'])

  def p_sample(model, x, t, t_index):
      betas_t = extract(betas, t, x.shape)
      sqrt_one_minus_alphas_cumprod_t = extract(
          sqrt_one_minus_alphas_cumprod, t, x.shape
      )
      sqrt_recip_alphas_t = extract(sqrt_recip_alphas, t, x.shape)
      model_mean = sqrt_recip_alphas_t * (x - betas_t * model(x, t) / sqrt_one_minus_alphas_cumprod_t)

      if t_index == 0:
          return model_mean
      posterior_variance_t = extract(posterior_variance, t, x.shape)
      noise = randn_like(x)
      return model_mean + ops.sqrt(posterior_variance_t) * noise

  def p_sample_loop(model, shape):
      b = shape[0]
      # Start with the pure noise.
      img = randn(shape, dtype=None)
      imgs = []

      for i in tqdm(reversed(range(0, timesteps)), desc='sampling loop time step', total=timesteps):
          img = p_sample(model, img, ms.numpy.full((b,), i, dtype=mstype.int32), i)
          imgs.append(img.asnumpy())
      return imgs

  def sample(model, image_size, batch_size=16, channels=3):
      return p_sample_loop(model, shape=(batch_size, channels, image_size, image_size))

  # Defining a dynamic learning rate.
  lr = nn.cosine_decay_lr(min_lr=1e-7, max_lr=1e-4, total_step=10*3750, step_per_epoch=3750, decay_epoch=10)

  # Defining a U-Net model.
  unet_model = Unet(
      dim=image_size,
      channels=channels,
      dim_mults=(1, 2, 4,)
  )

  name_list = []
  for (name, par) in list(unet_model.parameters_and_names()):
      name_list.append(name)
  i = 0
  for item in list(unet_model.trainable_params()):
      item.name = name_list[i]
      i += 1

  # Define an optimizer.
  optimizer = nn.Adam(unet_model.trainable_params(), learning_rate=lr)
  loss_scaler = DynamicLossScaler(65536, 2, 1000)

  # Define the forward process.
  def forward_fn(data, t, noise=None):
      loss = p_losses(unet_model, data, t, noise)
      return loss

  # Calculate the gradient.
  grad_fn = ms.value_and_grad(forward_fn, None, optimizer.parameters, has_aux=False)

  # Update the gradient.
  def train_step(data, t, noise):
      loss, grads = grad_fn(data, t, noise)
      optimizer(grads)
      return loss

  import time

  epochs = 10

  iterator = dataset.create_tuple_iterator(num_epochs=epochs)
  for epoch in range(epochs):
      begin_time = time.time()
      for step, batch in enumerate(iterator):
          unet_model.set_train()
          batch_size = batch[0].shape[0]
          t = randint(0, timesteps, (batch_size,), dtype=ms.int32)
          noise = randn_like(batch[0])
          loss = train_step(batch[0], t, noise)

          if step % 500 == 0:
              print(" epoch: ", epoch, " step: ", step, " Loss: ", loss)
      end_time = time.time()
      times = end_time - begin_time
      print("training time:", times, "s")
      # Display the random sampling effect.
      unet_model.set_train(False)
      samples = sample(unet_model, image_size=image_size, batch_size=64, channels=channels)
      plt.imshow(samples[-1][5].reshape(image_size, image_size, channels), cmap="gray")
  print("Training Success!")

  # Sample 64 images.
  unet_model.set_train(False)
  samples = sample(unet_model, image_size=image_size, batch_size=64, channels=channels)

  # Display a random one.
  random_index = 5
  plt.imshow(samples[-1][random_index].reshape(image_size, image_size, channels), cmap="gray")

  import matplotlib.animation as animation

  random_index = 53

  fig = plt.figure()
  ims = []
  for i in range(timesteps):
      im = plt.imshow(samples[i][random_index].reshape(image_size, image_size, channels), cmap="gray", animated=True)
      ims.append([im])

  animate = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=100)
  animate.save('diffusion.gif')
  plt.show()
  """

  print(dfm)