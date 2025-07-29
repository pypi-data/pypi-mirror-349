# FCN MODEL
def fcn():

  fcnm = """
  from download import download

  url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/dataset_fcn8s.tar"

  download(url, "./dataset", kind="tar", replace=True)

  import numpy as np
  import cv2
  import mindspore.dataset as ds

  class SegDataset:
      def __init__(self,
                  image_mean,
                  image_std,
                  data_file='',
                  batch_size=32,
                  crop_size=512,
                  max_scale=2.0,
                  min_scale=0.5,
                  ignore_label=255,
                  num_classes=21,
                  num_readers=2,
                  num_parallel_calls=4):

          self.data_file = data_file
          self.batch_size = batch_size
          self.crop_size = crop_size
          self.image_mean = np.array(image_mean, dtype=np.float32)
          self.image_std = np.array(image_std, dtype=np.float32)
          self.max_scale = max_scale
          self.min_scale = min_scale
          self.ignore_label = ignore_label
          self.num_classes = num_classes
          self.num_readers = num_readers
          self.num_parallel_calls = num_parallel_calls
          max_scale > min_scale

      def preprocess_dataset(self, image, label):
          image_out = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), cv2.IMREAD_COLOR)
          label_out = cv2.imdecode(np.frombuffer(label, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
          sc = np.random.uniform(self.min_scale, self.max_scale)
          new_h, new_w = int(sc * image_out.shape[0]), int(sc * image_out.shape[1])
          image_out = cv2.resize(image_out, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
          label_out = cv2.resize(label_out, (new_w, new_h), interpolation=cv2.INTER_NEAREST)

          image_out = (image_out - self.image_mean) / self.image_std
          out_h, out_w = max(new_h, self.crop_size), max(new_w, self.crop_size)
          pad_h, pad_w = out_h - new_h, out_w - new_w
          if pad_h > 0 or pad_w > 0:
              image_out = cv2.copyMakeBorder(image_out, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=0)
              label_out = cv2.copyMakeBorder(label_out, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=self.ignore_label)
          offset_h = np.random.randint(0, out_h - self.crop_size + 1)
          offset_w = np.random.randint(0, out_w - self.crop_size + 1)
          image_out = image_out[offset_h: offset_h + self.crop_size, offset_w: offset_w + self.crop_size, :]
          label_out = label_out[offset_h: offset_h + self.crop_size, offset_w: offset_w+self.crop_size]
          if np.random.uniform(0.0, 1.0) > 0.5:
              image_out = image_out[:, ::-1, :]
              label_out = label_out[:, ::-1]
          image_out = image_out.transpose((2, 0, 1))
          image_out = image_out.copy()
          label_out = label_out.copy()
          label_out = label_out.astype("int32")
          return image_out, label_out

      def get_dataset(self):
          ds.config.set_numa_enable(True)
          dataset = ds.MindDataset(self.data_file, columns_list=["data", "label"],
                                  shuffle=True, num_parallel_workers=self.num_readers)
          transforms_list = self.preprocess_dataset
          dataset = dataset.map(operations=transforms_list, input_columns=["data", "label"],
                                output_columns=["data", "label"],
                                num_parallel_workers=self.num_parallel_calls)
          dataset = dataset.shuffle(buffer_size=self.batch_size * 10)
          dataset = dataset.batch(self.batch_size, drop_remainder=True)
          return dataset


  # Define parameters for creating a dataset.
  IMAGE_MEAN = [103.53, 116.28, 123.675]
  IMAGE_STD = [57.375, 57.120, 58.395]
  DATA_FILE = "dataset/dataset_fcn8s/mindname.mindrecord"

  # Define model training parameters.
  train_batch_size = 4
  crop_size = 512
  min_scale = 0.5
  max_scale = 2.0
  ignore_label = 255
  num_classes = 21

  # Instantiate a dataset.
  dataset = SegDataset(image_mean=IMAGE_MEAN,
                      image_std=IMAGE_STD,
                      data_file=DATA_FILE,
                      batch_size=train_batch_size,
                      crop_size=crop_size,
                      max_scale=max_scale,
                      min_scale=min_scale,
                      ignore_label=ignore_label,
                      num_classes=num_classes,
                      num_readers=2,
                      num_parallel_calls=4)

  dataset = dataset.get_dataset()

  import numpy as np
  import matplotlib.pyplot as plt

  plt.figure(figsize=(16, 8))

  # Display data in the training set.
  for i in range(1, 9):
      plt.subplot(2, 4, i)
      show_data = next(dataset.create_dict_iterator())
      show_images = show_data["data"].asnumpy()
      show_images = np.clip(show_images, 0, 1)
  # Convert the image to the HWC format and display it.
      plt.imshow(show_images[0].transpose(1, 2, 0))
      plt.axis("off")
      plt.subplots_adjust(wspace=0.05, hspace=0)
  plt.show()

  import mindspore.nn as nn

  class FCN8s(nn.Cell):
      def __init__(self, n_class):
          super().__init__()
          self.n_class = n_class
          self.conv1 = nn.SequentialCell(
              nn.Conv2d(in_channels=3, out_channels=64,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(64),
              nn.ReLU(),
              nn.Conv2d(in_channels=64, out_channels=64,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(64),
              nn.ReLU()
          )
          self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
          self.conv2 = nn.SequentialCell(
              nn.Conv2d(in_channels=64, out_channels=128,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(128),
              nn.ReLU(),
              nn.Conv2d(in_channels=128, out_channels=128,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(128),
              nn.ReLU()
          )
          self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
          self.conv3 = nn.SequentialCell(
              nn.Conv2d(in_channels=128, out_channels=256,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(256),
              nn.ReLU(),
              nn.Conv2d(in_channels=256, out_channels=256,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(256),
              nn.ReLU(),
              nn.Conv2d(in_channels=256, out_channels=256,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(256),
              nn.ReLU()
          )
          self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
          self.conv4 = nn.SequentialCell(
              nn.Conv2d(in_channels=256, out_channels=512,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(512),
              nn.ReLU(),
              nn.Conv2d(in_channels=512, out_channels=512,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(512),
              nn.ReLU(),
              nn.Conv2d(in_channels=512, out_channels=512,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(512),
              nn.ReLU()
          )
          self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)
          self.conv5 = nn.SequentialCell(
              nn.Conv2d(in_channels=512, out_channels=512,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(512),
              nn.ReLU(),
              nn.Conv2d(in_channels=512, out_channels=512,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(512),
              nn.ReLU(),
              nn.Conv2d(in_channels=512, out_channels=512,
                        kernel_size=3, weight_init='xavier_uniform'),
              nn.BatchNorm2d(512),
              nn.ReLU()
          )
          self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2)
          self.conv6 = nn.SequentialCell(
              nn.Conv2d(in_channels=512, out_channels=4096,
                        kernel_size=7, weight_init='xavier_uniform'),
              nn.BatchNorm2d(4096),
              nn.ReLU(),
          )
          self.conv7 = nn.SequentialCell(
              nn.Conv2d(in_channels=4096, out_channels=4096,
                        kernel_size=1, weight_init='xavier_uniform'),
              nn.BatchNorm2d(4096),
              nn.ReLU(),
          )
          self.score_fr = nn.Conv2d(in_channels=4096, out_channels=self.n_class,
                                    kernel_size=1, weight_init='xavier_uniform')
          self.upscore2 = nn.Conv2dTranspose(in_channels=self.n_class, out_channels=self.n_class,
                                            kernel_size=4, stride=2, weight_init='xavier_uniform')
          self.score_pool4 = nn.Conv2d(in_channels=512, out_channels=self.n_class,
                                      kernel_size=1, weight_init='xavier_uniform')
          self.upscore_pool4 = nn.Conv2dTranspose(in_channels=self.n_class, out_channels=self.n_class,
                                                  kernel_size=4, stride=2, weight_init='xavier_uniform')
          self.score_pool3 = nn.Conv2d(in_channels=256, out_channels=self.n_class,
                                      kernel_size=1, weight_init='xavier_uniform')
          self.upscore8 = nn.Conv2dTranspose(in_channels=self.n_class, out_channels=self.n_class,
                                            kernel_size=16, stride=8, weight_init='xavier_uniform')

      def construct(self, x):
          x1 = self.conv1(x)
          p1 = self.pool1(x1)
          x2 = self.conv2(p1)
          p2 = self.pool2(x2)
          x3 = self.conv3(p2)
          p3 = self.pool3(x3)
          x4 = self.conv4(p3)
          p4 = self.pool4(x4)
          x5 = self.conv5(p4)
          p5 = self.pool5(x5)
          x6 = self.conv6(p5)
          x7 = self.conv7(x6)
          sf = self.score_fr(x7)
          u2 = self.upscore2(sf)
          s4 = self.score_pool4(p4)
          f4 = s4 + u2
          u4 = self.upscore_pool4(f4)
          s3 = self.score_pool3(p3)
          f3 = s3 + u4
          out = self.upscore8(f3)
          return out

  from download import download
  from mindspore import load_checkpoint, load_param_into_net

  url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/fcn8s_vgg16_pretrain.ckpt"
  download(url, "fcn8s_vgg16_pretrain.ckpt", replace=True)
  def load_vgg16():
      ckpt_vgg16 = "fcn8s_vgg16_pretrain.ckpt"
      param_vgg = load_checkpoint(ckpt_vgg16)
      load_param_into_net(net, param_vgg)

  import numpy as np
  import mindspore as ms
  import mindspore.nn as nn
  import mindspore.train as train

  class PixelAccuracy(train.Metric):
      def __init__(self, num_class=21):
          super(PixelAccuracy, self).__init__()
          self.num_class = num_class

      def _generate_matrix(self, gt_image, pre_image):
          mask = (gt_image >= 0) & (gt_image < self.num_class)
          label = self.num_class * gt_image[mask].astype('int') + pre_image[mask]
          count = np.bincount(label, minlength=self.num_class**2)
          confusion_matrix = count.reshape(self.num_class, self.num_class)
          return confusion_matrix

      def clear(self):
          self.confusion_matrix = np.zeros((self.num_class,) * 2)

      def update(self, *inputs):
          y_pred = inputs[0].asnumpy().argmax(axis=1)
          y = inputs[1].asnumpy().reshape(4, 512, 512)
          self.confusion_matrix += self._generate_matrix(y, y_pred)

      def eval(self):
          pixel_accuracy = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()
          return pixel_accuracy


  class PixelAccuracyClass(train.Metric):
      def __init__(self, num_class=21):
          super(PixelAccuracyClass, self).__init__()
          self.num_class = num_class

      def _generate_matrix(self, gt_image, pre_image):
          mask = (gt_image >= 0) & (gt_image < self.num_class)
          label = self.num_class * gt_image[mask].astype('int') + pre_image[mask]
          count = np.bincount(label, minlength=self.num_class**2)
          confusion_matrix = count.reshape(self.num_class, self.num_class)
          return confusion_matrix

      def update(self, *inputs):
          y_pred = inputs[0].asnumpy().argmax(axis=1)
          y = inputs[1].asnumpy().reshape(4, 512, 512)
          self.confusion_matrix += self._generate_matrix(y, y_pred)

      def clear(self):
          self.confusion_matrix = np.zeros((self.num_class,) * 2)

      def eval(self):
          mean_pixel_accuracy = np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=1)
          mean_pixel_accuracy = np.nanmean(mean_pixel_accuracy)
          return mean_pixel_accuracy


  class MeanIntersectionOverUnion(train.Metric):
      def __init__(self, num_class=21):
          super(MeanIntersectionOverUnion, self).__init__()
          self.num_class = num_class

      def _generate_matrix(self, gt_image, pre_image):
          mask = (gt_image >= 0) & (gt_image < self.num_class)
          label = self.num_class * gt_image[mask].astype('int') + pre_image[mask]
          count = np.bincount(label, minlength=self.num_class**2)
          confusion_matrix = count.reshape(self.num_class, self.num_class)
          return confusion_matrix

      def update(self, *inputs):
          y_pred = inputs[0].asnumpy().argmax(axis=1)
          y = inputs[1].asnumpy().reshape(4, 512, 512)
          self.confusion_matrix += self._generate_matrix(y, y_pred)

      def clear(self):
          self.confusion_matrix = np.zeros((self.num_class,) * 2)

      def eval(self):
          mean_iou = np.diag(self.confusion_matrix) / (
              np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
              np.diag(self.confusion_matrix))
          mean_iou = np.nanmean(mean_iou)
          return mean_iou


  class FrequencyWeightedIntersectionOverUnion(train.Metric):
      def __init__(self, num_class=21):
          super(FrequencyWeightedIntersectionOverUnion, self).__init__()
          self.num_class = num_class

      def _generate_matrix(self, gt_image, pre_image):
          mask = (gt_image >= 0) & (gt_image < self.num_class)
          label = self.num_class * gt_image[mask].astype('int') + pre_image[mask]
          count = np.bincount(label, minlength=self.num_class**2)
          confusion_matrix = count.reshape(self.num_class, self.num_class)
          return confusion_matrix

      def update(self, *inputs):
          y_pred = inputs[0].asnumpy().argmax(axis=1)
          y = inputs[1].asnumpy().reshape(4, 512, 512)
          self.confusion_matrix += self._generate_matrix(y, y_pred)

      def clear(self):
          self.confusion_matrix = np.zeros((self.num_class,) * 2)

      def eval(self):
          freq = np.sum(self.confusion_matrix, axis=1) / np.sum(self.confusion_matrix)
          iu = np.diag(self.confusion_matrix) / (
              np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
              np.diag(self.confusion_matrix))

          frequency_weighted_iou = (freq[freq > 0] * iu[freq > 0]).sum()
          return frequency_weighted_iou

  import mindspore
  from mindspore import Tensor
  import mindspore.nn as nn
  from mindspore.train import ModelCheckpoint, CheckpointConfig, LossMonitor, TimeMonitor, Model

  train_batch_size = 4
  num_classes = 21
  # Initialize the model structure.
  net = FCN8s(n_class=21)
  # Import VGG-16 pre-trained parameters.
  load_vgg16()
  # Calculate the learning rate.
  min_lr = 0.0005
  base_lr = 0.05
  train_epochs = 1
  iters_per_epoch = dataset.get_dataset_size()
  total_step = iters_per_epoch * train_epochs

  lr_scheduler = mindspore.nn.cosine_decay_lr(min_lr,
                                              base_lr,
                                              total_step,
                                              iters_per_epoch,
                                              decay_epoch=2)
  lr = Tensor(lr_scheduler[-1])

  # Define the loss function.
  loss = nn.CrossEntropyLoss(ignore_index=255)
  # Define the optimizer.
  optimizer = nn.Momentum(params=net.trainable_params(), learning_rate=lr, momentum=0.9, weight_decay=0.0001)
  # Define loss_scale.
  scale_factor = 4
  scale_window = 3000
  loss_scale_manager = ms.amp.DynamicLossScaleManager(scale_factor, scale_window)
  # Initialize the model.
  model = Model(net, loss_fn=loss, optimizer=optimizer, loss_scale_manager=loss_scale_manager, metrics={"pixel accuracy": PixelAccuracy(), "mean pixel accuracy": PixelAccuracyClass(), "mean IoU": MeanIntersectionOverUnion(), "frequency weighted IoU": FrequencyWeightedIntersectionOverUnion()})

  # Set the parameters for saving the CKPT file.
  time_callback = TimeMonitor(data_size=iters_per_epoch)
  loss_callback = LossMonitor()
  callbacks = [time_callback, loss_callback]
  save_steps = 330
  keep_checkpoint_max = 5
  config_ckpt = CheckpointConfig(save_checkpoint_steps=10,
                                keep_checkpoint_max=keep_checkpoint_max)
  ckpt_callback = ModelCheckpoint(prefix="FCN8s",
                                  directory="./ckpt",
                                  config=config_ckpt)
  callbacks.append(ckpt_callback)
  model.train(train_epochs, dataset, callbacks=callbacks)

  IMAGE_MEAN = [103.53, 116.28, 123.675]
  IMAGE_STD = [57.375, 57.120, 58.395]
  DATA_FILE = "dataset/dataset_fcn8s/mindname.mindrecord"

  # Download the trained weight file.
  url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/FCN8s.ckpt"
  download(url, "FCN8s.ckpt", replace=True)
  net = FCN8s(n_class=num_classes)

  ckpt_file = "FCN8s.ckpt"
  param_dict = load_checkpoint(ckpt_file)
  load_param_into_net(net, param_dict)

  model = Model(net, loss_fn=loss, optimizer=optimizer, loss_scale_manager=loss_scale_manager, metrics={"pixel accuracy": PixelAccuracy(), "mean pixel accuracy": PixelAccuracyClass(), "mean IoU": MeanIntersectionOverUnion(), "frequency weighted IoU": FrequencyWeightedIntersectionOverUnion()})

  # Instantiate a dataset.
  dataset = SegDataset(image_mean=IMAGE_MEAN,
                      image_std=IMAGE_STD,
                      data_file=DATA_FILE,
                      batch_size=train_batch_size,
                      crop_size=crop_size,
                      max_scale=max_scale,
                      min_scale=min_scale,
                      ignore_label=ignore_label,
                      num_classes=num_classes,
                      num_readers=2,
                      num_parallel_calls=4)
  dataset_eval = dataset.get_dataset()
  model.eval(dataset_eval)

  import cv2
  import matplotlib.pyplot as plt

  net = FCN8s(n_class=num_classes)
  # Set hyperparameters.
  ckpt_file = "FCN8s.ckpt"
  param_dict = load_checkpoint(ckpt_file)
  load_param_into_net(net, param_dict)
  eval_batch_size = 4
  img_lst = []
  mask_lst = []
  res_lst = []
  # Inference effect display (The upper part is the input image, and the lower part is the inference effect image.)
  plt.figure(figsize=(8, 5))
  show_data = next(dataset_eval.create_dict_iterator())
  show_images = show_data["data"].asnumpy()
  mask_images = show_data["label"].reshape([4, 512, 512])
  show_images = np.clip(show_images, 0, 1)
  for i in range(eval_batch_size):
      img_lst.append(show_images[i])
      mask_lst.append(mask_images[i])
  res = net(show_data["data"]).asnumpy().argmax(axis=1)
  for i in range(eval_batch_size):
      plt.subplot(2, 4, i + 1)
      plt.imshow(img_lst[i].transpose(1, 2, 0))
      plt.axis("off")
      plt.subplots_adjust(wspace=0.05, hspace=0.02)
      plt.subplot(2, 4, i + 5)
      plt.imshow(res[i])
      plt.axis("off")
      plt.subplots_adjust(wspace=0.05, hspace=0.02)
  plt.show()
  """
  print(fcnm)

# gan for image generation
def gan_for_image_generation():
  gfig = """
  from download import download

  url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/MNIST_Data.zip"

  download(url, "./", kind="zip", replace=True)

  import numpy as np
  import mindspore.dataset as ds

  batch_size = 128
  latent_size = 100 # Length of the implicit vector.

  train_dataset = ds.MnistDataset(dataset_dir='./MNIST_Data/train')
  test_dataset = ds.MnistDataset(dataset_dir='./MNIST_Data/test')

  def data_load(dataset):
      dataset1 = ds.GeneratorDataset(dataset, ["image", "label"], shuffle=True, python_multiprocessing=False)
      # Data augmentation
      mnist_ds = dataset1.map(
          operations=lambda x: (x.astype("float32"), np.random.normal(size=latent_size).astype("float32")),
          output_columns=["image", "latent_code"])
      mnist_ds = mnist_ds.project(["image", "latent_code"])

      # Batch operations
      mnist_ds = mnist_ds.batch(batch_size, True)

      return mnist_ds

  mnist_ds = data_load(train_dataset)

  iter_size = mnist_ds.get_dataset_size()
  print('Iter size: %d' % iter_size)

  import matplotlib.pyplot as plt

  data_iter = next(mnist_ds.create_dict_iterator(output_numpy=True))
  figure = plt.figure(figsize=(3, 3))
  cols, rows = 5, 5
  for idx in range(1, cols * rows + 1):
      image = data_iter['image'][idx]
      figure.add_subplot(rows, cols, idx)
      plt.axis("off")
      plt.imshow(image.squeeze(), cmap="gray")
  plt.show()

  import random
  import numpy as np
  from mindspore import Tensor
  from mindspore import dtype

  # Create a batch of implicit vectors using random seeds.
  np.random.seed(2323)
  test_noise = Tensor(np.random.normal(size=(25, 100)), dtype.float32)
  random.shuffle(test_noise)

  from mindspore import nn
  import mindspore.ops as ops

  img_size = 28 # Training image length (width)

  class Generator(nn.Cell):
      def __init__(self, latent_size, auto_prefix=True):
          super(Generator, self).__init__(auto_prefix=auto_prefix)
          self.model = nn.SequentialCell()
          # [N, 100] -> [N, 128]
          # Input a 100-dimensional Gaussian distribution between 0 and 1, and then map it to 256 dimensions through the first-layer linear transformation.
          self.model.append(nn.Dense(latent_size, 128))
          self.model.append(nn.ReLU())
          # [N, 128] -> [N, 256]
          self.model.append(nn.Dense(128, 256))
          self.model.append(nn.BatchNorm1d(256))
          self.model.append(nn.ReLU())
          # [N, 256] -> [N, 512]
          self.model.append(nn.Dense(256, 512))
          self.model.append(nn.BatchNorm1d(512))
          self.model.append(nn.ReLU())
          # [N, 512] -> [N, 1024]
          self.model.append(nn.Dense(512, 1024))
          self.model.append(nn.BatchNorm1d(1024))
          self.model.append(nn.ReLU())
          # [N, 1024] -> [N, 784]
          # It is converted into 784 dimensions through linear transformation.
          self.model.append(nn.Dense(1024, img_size * img_size))
          # After the Tanh activation function is used, the generated fake image data distribution is expected to range from -1 to 1.
          self.model.append(nn.Tanh())

      def construct(self, x):
          img = self.model(x)
          return ops.reshape(img, (-1, 1, 28, 28))

  net_g = Generator(latent_size)
  net_g.update_parameters_name('generator')

  # Discriminator
  class Discriminator(nn.Cell):
      def __init__(self, auto_prefix=True):
          super().__init__(auto_prefix=auto_prefix)
          self.model = nn.SequentialCell()
          # [N, 784] -> [N, 512]
          self.model.append(nn.Dense(img_size * img_size, 512))  # The number of input features is 784, and the number of output features is 512.
          self.model.append(nn.LeakyReLU())  # Nonlinear mapping activation function with a default slope of 0.2.
          # [N, 512] -> [N, 256]
          self.model.append(nn.Dense(512, 256)) # Linear mapping.
          self.model.append(nn.LeakyReLU())
          # [N, 256] -> [N, 1]
          self.model.append(nn.Dense(256, 1))
          self.model.append(nn.Sigmoid())  # Binary activation function, which maps real numbers to [0,1]

      def construct(self, x):
          x_flat = ops.reshape(x, (-1, img_size * img_size))
          return self.model(x_flat)

  net_d = Discriminator()
  net_d.update_parameters_name('discriminator')

  lr = 0.0002 # Learning rate

  # Loss function
  adversarial_loss = nn.BCELoss(reduction='mean')

  # Optimizers
  optimizer_d = nn.Adam(net_d.trainable_params(), learning_rate=lr, beta1=0.5, beta2=0.999)
  optimizer_g = nn.Adam(net_g.trainable_params(), learning_rate=lr, beta1=0.5, beta2=0.999)
  optimizer_g.update_parameters_name('optim_g')
  optimizer_d.update_parameters_name('optim_d')

  import os
  import time
  import matplotlib.pyplot as plt
  import mindspore as ms
  from mindspore import Tensor, save_checkpoint

  total_epoch = 200  # Number of training epochs
  batch_size = 128  # Batch size of the training set used for training

  # Parameters for loading a pre-trained model
  pred_trained = False
  pred_trained_g = './result/checkpoints/Generator99.ckpt'
  pred_trained_d = './result/checkpoints/Discriminator99.ckpt'

  checkpoints_path = "./result/checkpoints"  # Path for saving results
  image_path = "./result/images"  # Path for saving test results

  # Loss calculation process of the generator
  def generator_forward(test_noises):
      fake_data = net_g(test_noises)
      fake_out = net_d(fake_data)
      loss_g = adversarial_loss(fake_out, ops.ones_like(fake_out))
      return loss_g

  # Loss calculation process of the discriminator
  def discriminator_forward(real_data, test_noises):
      fake_data = net_g(test_noises)
      fake_out = net_d(fake_data)
      real_out = net_d(real_data)
      real_loss = adversarial_loss(real_out, ops.ones_like(real_out))
      fake_loss = adversarial_loss(fake_out, ops.zeros_like(fake_out))
      loss_d = real_loss + fake_loss
      return loss_d

  # Gradient method
  grad_g = ms.value_and_grad(generator_forward, None, net_g.trainable_params())
  grad_d = ms.value_and_grad(discriminator_forward, None, net_d.trainable_params())

  def train_step(real_data, latent_code):
      # Calculate discriminator loss and gradient.
      loss_d, grads_d = grad_d(real_data, latent_code)
      optimizer_d(grads_d)
      loss_g, grads_g = grad_g(latent_code)
      optimizer_g(grads_g)

      return loss_d, loss_g

  # Save the generated test image.
  def save_imgs(gen_imgs1, idx):
      for i3 in range(gen_imgs1.shape[0]):
          plt.subplot(5, 5, i3 + 1)
          plt.imshow(gen_imgs1[i3, 0, :, :] / 2 + 0.5, cmap="gray")
          plt.axis("off")
      plt.savefig(image_path + "/test_{}.png".format(idx))

  # Set the path for saving parameters.
  os.makedirs(checkpoints_path, exist_ok=True)
  # Set the path for saving the images generated during the intermediate process.
  os.makedirs(image_path, exist_ok=True)

  net_g.set_train()
  net_d.set_train()

  # Store the generator and discriminator loss.
  losses_g, losses_d = [], []

  for epoch in range(total_epoch):
      start = time.time()
      for (iter, data) in enumerate(mnist_ds):
          start1 = time.time()
          image, latent_code = data
          image = (image - 127.5) / 127.5  # [0, 255] -> [-1, 1]
          image = image.reshape(image.shape[0], 1, image.shape[1], image.shape[2])
          d_loss, g_loss = train_step(image, latent_code)
          end1 = time.time()
          if iter % 10 == 0:
              print(f"Epoch:[{int(epoch):>3d}/{int(total_epoch):>3d}], "
                    f"step:[{int(iter):>4d}/{int(iter_size):>4d}], "
                    f"loss_d:{d_loss.asnumpy():>4f} , "
                    f"loss_g:{g_loss.asnumpy():>4f} , "
                    f"time:{(end1 - start1):>3f}s, "
                    f"lr:{lr:>6f}")

      end = time.time()
      print("time of epoch {} is {:.2f}s".format(epoch + 1, end - start))

      losses_d.append(d_loss.asnumpy())
      losses_g.append(g_loss.asnumpy())

      # After each epoch ends, use the generator to generate a group of images.
      gen_imgs = net_g(test_noise)
      save_imgs(gen_imgs.asnumpy(), epoch)

      # Save the model weight file based on the epoch.
      if epoch % 1 == 0:
          save_checkpoint(net_g, checkpoints_path + "/Generator%d.ckpt" % (epoch))
          save_checkpoint(net_d, checkpoints_path + "/Discriminator%d.ckpt" % (epoch))

  plt.figure(figsize=(6, 4))
  plt.title("Generator and Discriminator Loss During Training")
  plt.plot(losses_g, label="G", color='blue')
  plt.plot(losses_d, label="D", color='orange')
  plt.xlim(-20, 220)
  plt.ylim(0, 3.5)
  plt.xlabel("iterations")
  plt.ylabel("Loss")
  plt.legend()
  plt.show()

  import cv2
  import matplotlib.animation as animation

  # Convert the test image generated during training to a dynamic image.
  image_list = []
  for i in range(total_epoch):
      image_list.append(cv2.imread(image_path + "/test_{}.png".format(i), cv2.IMREAD_GRAYSCALE))
  show_list = []
  fig = plt.figure(dpi=70)
  for epoch in range(0, len(image_list), 5):
      plt.axis("off")
      show_list.append([plt.imshow(image_list[epoch], cmap='gray')])

  ani = animation.ArtistAnimation(fig, show_list, interval=1000, repeat_delay=1000, blit=True)
  ani.save('train_test.gif', writer='pillow', fps=1)

  import mindspore as ms

  test_ckpt = './result/checkpoints/Generator199.ckpt'

  parameter = ms.load_checkpoint(test_ckpt)
  ms.load_param_into_net(net_g, parameter)
  # Model generation result
  test_data = Tensor(np.random.normal(0, 1, (25, 100)).astype(np.float32))
  images = net_g(test_data).transpose(0, 2, 3, 1).asnumpy()
  # Result display
  fig = plt.figure(figsize=(3, 3), dpi=120)
  for i in range(25):
      fig.add_subplot(5, 5, i + 1)
      plt.axis("off")
      plt.imshow(images[i].squeeze(), cmap="gray")
  plt.show()
  """
  print(gfig)

## 
def Generating_cartoon_head_portraits_via_DCGAN():
  gchpvd = """
  # Generating_cartoon_head_portraits_via_DCGAN_.ipynb
  from download import download

  url = "https://download.mindspore.cn/dataset/Faces/faces.zip"

  path = download(url, "./faces", kind="zip", replace=True)

  batch_size = 128          # Batch size
  image_size = 64           # Size of the training image
  nc = 3                    # Number of color channels
  nz = 100                  # Length of the implicit vector
  ngf = 64                  # Size of the feature map in the generator
  ndf = 64                  # Size of the feature map in the discriminator
  num_epochs = 10           # Number of training epochs
  lr = 0.0002               # Learning rate
  beta1 = 0.5               # Beta 1 hyperparameter of the Adam optimizer

  import numpy as np
  import mindspore.dataset as ds
  import mindspore.dataset.vision as vision

  def create_dataset_imagenet(dataset_path):
      dataset = ds.ImageFolderDataset(dataset_path,
                                      num_parallel_workers=4,
                                      shuffle=True,
                                      decode=True)

      # Data augmentation
      transforms = [
          vision.Resize(image_size),
          vision.CenterCrop(image_size),
          vision.HWC2CHW(),
          lambda x: ((x / 255).astype("float32"))
      ]

      # Data mapping
      dataset = dataset.project('image')
      dataset = dataset.map(transforms, 'image')

      # Batch operation
      dataset = dataset.batch(batch_size)
      return dataset

  dataset = create_dataset_imagenet('./faces')

  import matplotlib.pyplot as plt

  def plot_data(data):
      # Visualize some traing data.
      plt.figure(figsize=(10, 3), dpi=140)
      for i, image in enumerate(data[0][:30], 1):
          plt.subplot(3, 10, i)
          plt.axis("off")
          plt.imshow(image.transpose(1, 2, 0))
      plt.show()

  sample_data = next(dataset.create_tuple_iterator(output_numpy=True))
  plot_data(sample_data)

  import mindspore as ms
  from mindspore import nn, ops
  from mindspore.common.initializer import Normal

  weight_init = Normal(mean=0, sigma=0.02)
  gamma_init = Normal(mean=1, sigma=0.02)

  class Generator(nn.Cell):

      def __init__(self):
          super(Generator, self).__init__()
          self.generator = nn.SequentialCell(
              nn.Conv2dTranspose(nz, ngf * 8, 4, 1, 'valid', weight_init=weight_init),
              nn.BatchNorm2d(ngf * 8, gamma_init=gamma_init),
              nn.ReLU(),
              nn.Conv2dTranspose(ngf * 8, ngf * 4, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.BatchNorm2d(ngf * 4, gamma_init=gamma_init),
              nn.ReLU(),
              nn.Conv2dTranspose(ngf * 4, ngf * 2, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.BatchNorm2d(ngf * 2, gamma_init=gamma_init),
              nn.ReLU(),
              nn.Conv2dTranspose(ngf * 2, ngf, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.BatchNorm2d(ngf, gamma_init=gamma_init),
              nn.ReLU(),
              nn.Conv2dTranspose(ngf, nc, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.Tanh()
              )

      def construct(self, x):
          return self.generator(x)

  generator = Generator()

  class Discriminator(nn.Cell):

      def __init__(self):
          super(Discriminator, self).__init__()
          self.discriminator = nn.SequentialCell(
              nn.Conv2d(nc, ndf, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.LeakyReLU(0.2),
              nn.Conv2d(ndf, ndf * 2, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.BatchNorm2d(ndf * 2, gamma_init=gamma_init),
              nn.LeakyReLU(0.2),
              nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.BatchNorm2d(ndf * 4, gamma_init=gamma_init),
              nn.LeakyReLU(0.2),
              nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 'pad', 1, weight_init=weight_init),
              nn.BatchNorm2d(ndf * 8, gamma_init=gamma_init),
              nn.LeakyReLU(0.2),
              nn.Conv2d(ndf * 8, 1, 4, 1, 'valid', weight_init=weight_init),
              )
          self.adv_layer = nn.Sigmoid()

      def construct(self, x):
          out = self.discriminator(x)
          out = out.reshape(out.shape[0], -1)
          return self.adv_layer(out)

  discriminator = Discriminator()

  # Define loss function
  adversarial_loss = nn.BCELoss(reduction='mean')

  # Set optimizers for the generator and discriminator, respectively.
  optimizer_D = nn.Adam(discriminator.trainable_params(), learning_rate=lr, beta1=beta1)
  optimizer_G = nn.Adam(generator.trainable_params(), learning_rate=lr, beta1=beta1)
  optimizer_G.update_parameters_name('optim_g.')
  optimizer_D.update_parameters_name('optim_d.')

  def generator_forward(real_imgs, valid):
      # Sample noise as generator input
      z = ops.standard_normal((real_imgs.shape[0], nz, 1, 1))

      # Generate a batch of images
      gen_imgs = generator(z)

      # Loss measures generator's ability to fool the discriminator
      g_loss = adversarial_loss(discriminator(gen_imgs), valid)

      return g_loss, gen_imgs

  def discriminator_forward(real_imgs, gen_imgs, valid, fake):
      # Measure discriminator's ability to classify real from generated samples
      real_loss = adversarial_loss(discriminator(real_imgs), valid)
      fake_loss = adversarial_loss(discriminator(gen_imgs), fake)
      d_loss = (real_loss + fake_loss) / 2
      return d_loss

  grad_generator_fn = ms.value_and_grad(generator_forward, None,
                                        optimizer_G.parameters,
                                        has_aux=True)
  grad_discriminator_fn = ms.value_and_grad(discriminator_forward, None,
                                            optimizer_D.parameters)

  @ms.jit
  def train_step(imgs):
      valid = ops.ones((imgs.shape[0], 1), mindspore.float32)
      fake = ops.zeros((imgs.shape[0], 1), mindspore.float32)

      (g_loss, gen_imgs), g_grads = grad_generator_fn(imgs, valid)
      optimizer_G(g_grads)
      d_loss, d_grads = grad_discriminator_fn(imgs, gen_imgs, valid, fake)
      optimizer_D(d_grads)

      return g_loss, d_loss, gen_imgs

  import mindspore

  G_losses = []
  D_losses = []
  image_list = []

  total = dataset.get_dataset_size()
  iterator = dataset.create_tuple_iterator(num_epochs=num_epochs)
  for epoch in range(num_epochs):
      generator.set_train()
      discriminator.set_train()
      # Read in data for each training round
      for i, (imgs, ) in enumerate(iterator):
          g_loss, d_loss, gen_imgs = train_step(imgs)
          if i % 100 == 0 or i == total - 1:
              # Output training records
              print('[%2d/%d][%3d/%d]   Loss_D:%7.4f  Loss_G:%7.4f' % (
                  epoch + 1, num_epochs, i + 1, total, d_loss.asnumpy(), g_loss.asnumpy()))
          D_losses.append(d_loss.asnumpy())
          G_losses.append(g_loss.asnumpy())

      # After each epoch, use the generator to generate a set of images
      generator.set_train(False)
      fixed_noise = ops.standard_normal((batch_size, nz, 1, 1))
      img = generator(fixed_noise)
      image_list.append(img.transpose(0, 2, 3, 1).asnumpy())

      # Save the network model parameters as a ckpt file
      mindspore.save_checkpoint(generator, "./generator.ckpt")
      mindspore.save_checkpoint(discriminator, "./discriminator.ckpt")

  plt.figure(figsize=(10, 5))
  plt.title("Generator and Discriminator Loss During Training")
  plt.plot(G_losses, label="G", color='blue')
  plt.plot(D_losses, label="D", color='orange')
  plt.xlabel("iterations")
  plt.ylabel("Loss")
  plt.legend()
  plt.show()

  import matplotlib.pyplot as plt
  import matplotlib.animation as animation

  def showGif(image_list):
      show_list = []
      fig = plt.figure(figsize=(8, 3), dpi=120)
      for epoch in range(len(image_list)):
          images = []
          for i in range(3):
              row = np.concatenate((image_list[epoch][i * 8:(i + 1) * 8]), axis=1)
              images.append(row)
          img = np.clip(np.concatenate((images[:]), axis=0), 0, 1)
          plt.axis("off")
          show_list.append([plt.imshow(img)])

      ani = animation.ArtistAnimation(fig, show_list, interval=1000, repeat_delay=1000, blit=True)
      ani.save('./dcgan.gif', writer='pillow', fps=1)

  showGif(image_list)

  # Get the model parameters from the file and load them into the network
  mindspore.load_checkpoint("./generator.ckpt", generator)

  fixed_noise = ops.standard_normal((batch_size, nz, 1, 1))
  img64 = generator(fixed_noise).transpose(0, 2, 3, 1).asnumpy()

  fig = plt.figure(figsize=(8, 3), dpi=120)
  images = []
  for i in range(3):
      images.append(np.concatenate((img64[i * 8:(i + 1) * 8]), axis=1))
  img = np.clip(np.concatenate((images[:]), axis=0), 0, 1)
  plt.axis("off")
  plt.imshow(img)
  plt.show()
  """
  print(gchpvd)