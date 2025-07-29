## SDD
def sdd():
  sddite = """
  from download import download

  dataset_url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/ssd_datasets.zip"
  path = "./"
  path = download(dataset_url, path, kind="zip", replace=True)

  coco_root = "./datasets/"
  anno_json = "./datasets/annotations/instances_val2017.json"

  train_cls = ['background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
              'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
              'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
              'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
              'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
              'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
              'kite', 'baseball bat', 'baseball glove', 'skateboard',
              'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
              'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
              'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
              'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
              'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
              'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
              'refrigerator', 'book', 'clock', 'vase', 'scissors',
              'teddy bear', 'hair drier', 'toothbrush']

  train_cls_dict = {}
  for i, cls in enumerate(train_cls):
      train_cls_dict[cls] = i

  import cv2
  import numpy as np

  def _rand(a=0., b=1.):
      return np.random.rand() * (b - a) + a

  def intersect(box_a, box_b):
      # Compute the intersect of two sets of boxes.
      max_yx = np.minimum(box_a[:, 2:4], box_b[2:4])
      min_yx = np.maximum(box_a[:, :2], box_b[:2])
      inter = np.clip((max_yx - min_yx), a_min=0, a_max=np.inf)
      return inter[:, 0] * inter[:, 1]

  def jaccard_numpy(box_a, box_b):
      # Compute the jaccard overlap of two sets of boxes.
      inter = intersect(box_a, box_b)
      area_a = ((box_a[:, 2] - box_a[:, 0]) *
                (box_a[:, 3] - box_a[:, 1]))
      area_b = ((box_b[2] - box_b[0]) *
                (box_b[3] - box_b[1]))
      union = area_a + area_b - inter
      return inter / union

  def random_sample_crop(image, boxes):
      # Crop images and boxes randomly.
      height, width, _ = image.shape
      min_iou = np.random.choice([None, 0.1, 0.3, 0.5, 0.7, 0.9])

      if min_iou is None:
          return image, boxes

      for _ in range(50):
          image_t = image
          w = _rand(0.3, 1.0) * width
          h = _rand(0.3, 1.0) * height
          # aspect ratio constraint b/t .5 & 2
          if h / w < 0.5 or h / w > 2:
              continue

          left = _rand() * (width - w)
          top = _rand() * (height - h)
          rect = np.array([int(top), int(left), int(top + h), int(left + w)])
          overlap = jaccard_numpy(boxes, rect)

          # dropout some boxes
          drop_mask = overlap > 0
          if not drop_mask.any():
              continue

          if overlap[drop_mask].min() < min_iou and overlap[drop_mask].max() > (min_iou + 0.2):
              continue

          image_t = image_t[rect[0]:rect[2], rect[1]:rect[3], :]
          centers = (boxes[:, :2] + boxes[:, 2:4]) / 2.0
          m1 = (rect[0] < centers[:, 0]) * (rect[1] < centers[:, 1])
          m2 = (rect[2] > centers[:, 0]) * (rect[3] > centers[:, 1])

          # mask in that both m1 and m2 are true
          mask = m1 * m2 * drop_mask

          # have any valid boxes? try again if not
          if not mask.any():
              continue

          # take only matching gt boxes
          boxes_t = boxes[mask, :].copy()
          boxes_t[:, :2] = np.maximum(boxes_t[:, :2], rect[:2])
          boxes_t[:, :2] -= rect[:2]
          boxes_t[:, 2:4] = np.minimum(boxes_t[:, 2:4], rect[2:4])
          boxes_t[:, 2:4] -= rect[:2]

          return image_t, boxes_t
      return image, boxes

  def ssd_bboxes_encode(boxes):
      # Labels anchors with ground truth inputs.

      def jaccard_with_anchors(bbox):
          # Compute jaccard score a box and the anchors.
          # Intersection bbox and volume.
          ymin = np.maximum(y1, bbox[0])
          xmin = np.maximum(x1, bbox[1])
          ymax = np.minimum(y2, bbox[2])
          xmax = np.minimum(x2, bbox[3])
          w = np.maximum(xmax - xmin, 0.)
          h = np.maximum(ymax - ymin, 0.)

          # Volumes.
          inter_vol = h * w
          union_vol = vol_anchors + (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) - inter_vol
          jaccard = inter_vol / union_vol
          return np.squeeze(jaccard)

      pre_scores = np.zeros((8732), dtype=np.float32)
      t_boxes = np.zeros((8732, 4), dtype=np.float32)
      t_label = np.zeros((8732), dtype=np.int64)
      for bbox in boxes:
          label = int(bbox[4])
          scores = jaccard_with_anchors(bbox)
          idx = np.argmax(scores)
          scores[idx] = 2.0
          mask = (scores > matching_threshold)
          mask = mask & (scores > pre_scores)
          pre_scores = np.maximum(pre_scores, scores * mask)
          t_label = mask * label + (1 - mask) * t_label
          for i in range(4):
              t_boxes[:, i] = mask * bbox[i] + (1 - mask) * t_boxes[:, i]

      index = np.nonzero(t_label)

      # Transform to tlbr.
      bboxes = np.zeros((8732, 4), dtype=np.float32)
      bboxes[:, [0, 1]] = (t_boxes[:, [0, 1]] + t_boxes[:, [2, 3]]) / 2
      bboxes[:, [2, 3]] = t_boxes[:, [2, 3]] - t_boxes[:, [0, 1]]

      # Encode features.
      bboxes_t = bboxes[index]
      default_boxes_t = default_boxes[index]
      bboxes_t[:, :2] = (bboxes_t[:, :2] - default_boxes_t[:, :2]) / (default_boxes_t[:, 2:] * 0.1)
      tmp = np.maximum(bboxes_t[:, 2:4] / default_boxes_t[:, 2:4], 0.000001)
      bboxes_t[:, 2:4] = np.log(tmp) / 0.2
      bboxes[index] = bboxes_t

      num_match = np.array([len(np.nonzero(t_label)[0])], dtype=np.int32)
      return bboxes, t_label.astype(np.int32), num_match

  def preprocess_fn(img_id, image, box, is_training):
      # Preprocess function for dataset.
      cv2.setNumThreads(2)

      def _infer_data(image, input_shape):
          img_h, img_w, _ = image.shape
          input_h, input_w = input_shape

          image = cv2.resize(image, (input_w, input_h))

          # When the channels of image is 1
          if len(image.shape) == 2:
              image = np.expand_dims(image, axis=-1)
              image = np.concatenate([image, image, image], axis=-1)

          return img_id, image, np.array((img_h, img_w), np.float32)

      def _data_aug(image, box, is_training, image_size=(300, 300)):
          ih, iw, _ = image.shape
          h, w = image_size
          if not is_training:
              return _infer_data(image, image_size)
          # Random crop
          box = box.astype(np.float32)
          image, box = random_sample_crop(image, box)
          ih, iw, _ = image.shape
          # Resize image
          image = cv2.resize(image, (w, h))
          # Flip image or not
          flip = _rand() < .5
          if flip:
              image = cv2.flip(image, 1, dst=None)
          # When the channels of image is 1
          if len(image.shape) == 2:
              image = np.expand_dims(image, axis=-1)
              image = np.concatenate([image, image, image], axis=-1)
          box[:, [0, 2]] = box[:, [0, 2]] / ih
          box[:, [1, 3]] = box[:, [1, 3]] / iw
          if flip:
              box[:, [1, 3]] = 1 - box[:, [3, 1]]
          box, label, num_match = ssd_bboxes_encode(box)
          return image, box, label, num_match

      return _data_aug(image, box, is_training, image_size=[300, 300])

  from mindspore import Tensor
  from mindspore.dataset import MindDataset
  from mindspore.dataset.vision import Decode, HWC2CHW, Normalize, RandomColorAdjust


  def create_ssd_dataset(mindrecord_file, batch_size=32, device_num=1, rank=0,
                        is_training=True, num_parallel_workers=1, use_multiprocessing=True):
      # Create SSD dataset with MindDataset.
      dataset = MindDataset(mindrecord_file, columns_list=["img_id", "image", "annotation"], num_shards=device_num,
                            shard_id=rank, num_parallel_workers=num_parallel_workers, shuffle=is_training)

      decode = Decode()
      dataset = dataset.map(operations=decode, input_columns=["image"])

      change_swap_op = HWC2CHW()
      # Computed from random subset of ImageNet training images
      normalize_op = Normalize(mean=[0.485 * 255, 0.456 * 255, 0.406 * 255],
                              std=[0.229 * 255, 0.224 * 255, 0.225 * 255])
      color_adjust_op = RandomColorAdjust(brightness=0.4, contrast=0.4, saturation=0.4)
      compose_map_func = (lambda img_id, image, annotation: preprocess_fn(img_id, image, annotation, is_training))

      if is_training:
          output_columns = ["image", "box", "label", "num_match"]
          trans = [color_adjust_op, normalize_op, change_swap_op]
      else:
          output_columns = ["img_id", "image", "image_shape"]
          trans = [normalize_op, change_swap_op]

      dataset = dataset.map(operations=compose_map_func, input_columns=["img_id", "image", "annotation"],
                            output_columns=output_columns, python_multiprocessing=use_multiprocessing,
                            num_parallel_workers=num_parallel_workers)

      dataset = dataset.map(operations=trans, input_columns=["image"], python_multiprocessing=use_multiprocessing,
                            num_parallel_workers=num_parallel_workers)

      dataset = dataset.batch(batch_size, drop_remainder=True)
      return dataset

  from mindspore import nn

  def _make_layer(channels):
      in_channels = channels[0]
      layers = []
      for out_channels in channels[1:]:
          layers.append(nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3))
          layers.append(nn.ReLU())
          in_channels = out_channels
      return nn.SequentialCell(layers)

  class Vgg16(nn.Cell):
      # VGG16 module.

      def __init__(self):
          super(Vgg16, self).__init__()
          self.b1 = _make_layer([3, 64, 64])
          self.b2 = _make_layer([64, 128, 128])
          self.b3 = _make_layer([128, 256, 256, 256])
          self.b4 = _make_layer([256, 512, 512, 512])
          self.b5 = _make_layer([512, 512, 512, 512])

          self.m1 = nn.MaxPool2d(kernel_size=2, stride=2, pad_mode='SAME')
          self.m2 = nn.MaxPool2d(kernel_size=2, stride=2, pad_mode='SAME')
          self.m3 = nn.MaxPool2d(kernel_size=2, stride=2, pad_mode='SAME')
          self.m4 = nn.MaxPool2d(kernel_size=2, stride=2, pad_mode='SAME')
          self.m5 = nn.MaxPool2d(kernel_size=3, stride=1, pad_mode='SAME')

      def construct(self, x):
          # block1
          x = self.b1(x)
          x = self.m1(x)

          # block2
          x = self.b2(x)
          x = self.m2(x)

          # block3
          x = self.b3(x)
          x = self.m3(x)

          # block4
          x = self.b4(x)
          block4 = x
          x = self.m4(x)

          # block5
          x = self.b5(x)
          x = self.m5(x)

          return block4, x

  import mindspore as ms
  import mindspore.nn as nn
  import mindspore.ops as ops

  def _last_conv2d(in_channel, out_channel, kernel_size=3, stride=1, pad_mod='same', pad=0):
      in_channels = in_channel
      out_channels = in_channel
      depthwise_conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, pad_mode='same',
                                padding=pad, group=in_channels)
      conv = nn.Conv2d(in_channel, out_channel, kernel_size=1, stride=1, padding=0, pad_mode='same', has_bias=True)
      bn = nn.BatchNorm2d(in_channel, eps=1e-3, momentum=0.97,
                          gamma_init=1, beta_init=0, moving_mean_init=0, moving_var_init=1)

      return nn.SequentialCell([depthwise_conv, bn, nn.ReLU6(), conv])

  class FlattenConcat(nn.Cell):
      # FlattenConcat module.

      def __init__(self):
          super(FlattenConcat, self).__init__()
          self.num_ssd_boxes = 8732

      def construct(self, inputs):
          output = ()
          batch_size = ops.shape(inputs[0])[0]
          for x in inputs:
              x = ops.transpose(x, (0, 2, 3, 1))
              output += (ops.reshape(x, (batch_size, -1)),)
          res = ops.concat(output, axis=1)
          return ops.reshape(res, (batch_size, self.num_ssd_boxes, -1))

  class MultiBox(nn.Cell):
      # Multibox conv layers. Each multibox layer contains class conf scores and localization predictions.

      def __init__(self):
          super(MultiBox, self).__init__()
          num_classes = 81
          out_channels = [512, 1024, 512, 256, 256, 256]
          num_default = [4, 6, 6, 6, 4, 4]

          loc_layers = []
          cls_layers = []
          for k, out_channel in enumerate(out_channels):
              loc_layers += [_last_conv2d(out_channel, 4 * num_default[k],
                                          kernel_size=3, stride=1, pad_mod='same', pad=0)]
              cls_layers += [_last_conv2d(out_channel, num_classes * num_default[k],
                                          kernel_size=3, stride=1, pad_mod='same', pad=0)]

          self.multi_loc_layers = nn.CellList(loc_layers)
          self.multi_cls_layers = nn.CellList(cls_layers)
          self.flatten_concat = FlattenConcat()

      def construct(self, inputs):
          loc_outputs = ()
          cls_outputs = ()
          for i in range(len(self.multi_loc_layers)):
              loc_outputs += (self.multi_loc_layers[i](inputs[i]),)
              cls_outputs += (self.multi_cls_layers[i](inputs[i]),)
          return self.flatten_concat(loc_outputs), self.flatten_concat(cls_outputs)

  class SSD300Vgg16(nn.Cell):
      # SSD300Vgg16 module.

      def __init__(self):
          super(SSD300Vgg16, self).__init__()

          # VGG16 backbone: block1~5
          self.backbone = Vgg16()

          # SSD blocks: block6~7
          self.b6_1 = nn.Conv2d(in_channels=512, out_channels=1024, kernel_size=3, padding=6, dilation=6, pad_mode='pad')
          self.b6_2 = nn.Dropout(p=0.5)

          self.b7_1 = nn.Conv2d(in_channels=1024, out_channels=1024, kernel_size=1)
          self.b7_2 = nn.Dropout(p=0.5)

          # Extra Feature Layers: block8~11
          self.b8_1 = nn.Conv2d(in_channels=1024, out_channels=256, kernel_size=1, padding=1, pad_mode='pad')
          self.b8_2 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=2, pad_mode='valid')

          self.b9_1 = nn.Conv2d(in_channels=512, out_channels=128, kernel_size=1, padding=1, pad_mode='pad')
          self.b9_2 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, pad_mode='valid')

          self.b10_1 = nn.Conv2d(in_channels=256, out_channels=128, kernel_size=1)
          self.b10_2 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, pad_mode='valid')

          self.b11_1 = nn.Conv2d(in_channels=256, out_channels=128, kernel_size=1)
          self.b11_2 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, pad_mode='valid')

          # boxes
          self.multi_box = MultiBox()

      def construct(self, x):
          # VGG16 backbone: block1~5
          block4, x = self.backbone(x)

          # SSD blocks: block6~7
          x = self.b6_1(x)  # 1024
          x = self.b6_2(x)

          x = self.b7_1(x)  # 1024
          x = self.b7_2(x)
          block7 = x

          # Extra Feature Layers: block8~11
          x = self.b8_1(x)  # 256
          x = self.b8_2(x)  # 512
          block8 = x

          x = self.b9_1(x)  # 128
          x = self.b9_2(x)  # 256
          block9 = x

          x = self.b10_1(x)  # 128
          x = self.b10_2(x)  # 256
          block10 = x

          x = self.b11_1(x)  # 128
          x = self.b11_2(x)  # 256
          block11 = x

          # boxes
          multi_feature = (block4, block7, block8, block9, block10, block11)
          pred_loc, pred_label = self.multi_box(multi_feature)
          if not self.training:
              pred_label = ops.sigmoid(pred_label)
          pred_loc = pred_loc.astype(ms.float32)
          pred_label = pred_label.astype(ms.float32)
          return pred_loc, pred_label

  def class_loss(logits, label):
      # Calculate category losses.
      label = ops.one_hot(label, ops.shape(logits)[-1], Tensor(1.0, ms.float32), Tensor(0.0, ms.float32))
      weight = ops.ones_like(logits)
      pos_weight = ops.ones_like(logits)
      sigmiod_cross_entropy = ops.binary_cross_entropy_with_logits(logits, label, weight.astype(ms.float32), pos_weight.astype(ms.float32))
      sigmoid = ops.sigmoid(logits)
      label = label.astype(ms.float32)
      p_t = label * sigmoid + (1 - label) * (1 - sigmoid)
      modulating_factor = ops.pow(1 - p_t, 2.0)
      alpha_weight_factor = label * 0.75 + (1 - label) * (1 - 0.75)
      focal_loss = modulating_factor * alpha_weight_factor * sigmiod_cross_entropy
      return focal_loss

  import json
  from pycocotools.coco import COCO
  from pycocotools.cocoeval import COCOeval


  def apply_eval(eval_param_dict):
      net = eval_param_dict["net"]
      net.set_train(False)
      ds = eval_param_dict["dataset"]
      anno_json = eval_param_dict["anno_json"]
      coco_metrics = COCOMetrics(anno_json=anno_json,
                                classes=train_cls,
                                num_classes=81,
                                max_boxes=100,
                                nms_threshold=0.6,
                                min_score=0.1)
      for data in ds.create_dict_iterator(output_numpy=True, num_epochs=1):
          img_id = data['img_id']
          img_np = data['image']
          image_shape = data['image_shape']

          output = net(Tensor(img_np))

          for batch_idx in range(img_np.shape[0]):
              pred_batch = {
                  "boxes": output[0].asnumpy()[batch_idx],
                  "box_scores": output[1].asnumpy()[batch_idx],
                  "img_id": int(np.squeeze(img_id[batch_idx])),
                  "image_shape": image_shape[batch_idx]
              }
              coco_metrics.update(pred_batch)
      eval_metrics = coco_metrics.get_metrics()
      return eval_metrics


  def apply_nms(all_boxes, all_scores, thres, max_boxes):
      # Apply NMS to bboxes.
      y1 = all_boxes[:, 0]
      x1 = all_boxes[:, 1]
      y2 = all_boxes[:, 2]
      x2 = all_boxes[:, 3]
      areas = (x2 - x1 + 1) * (y2 - y1 + 1)

      order = all_scores.argsort()[::-1]
      keep = []

      while order.size > 0:
          i = order[0]
          keep.append(i)

          if len(keep) >= max_boxes:
              break

          xx1 = np.maximum(x1[i], x1[order[1:]])
          yy1 = np.maximum(y1[i], y1[order[1:]])
          xx2 = np.minimum(x2[i], x2[order[1:]])
          yy2 = np.minimum(y2[i], y2[order[1:]])

          w = np.maximum(0.0, xx2 - xx1 + 1)
          h = np.maximum(0.0, yy2 - yy1 + 1)
          inter = w * h

          ovr = inter / (areas[i] + areas[order[1:]] - inter)

          inds = np.where(ovr <= thres)[0]

          order = order[inds + 1]
      return keep


  class COCOMetrics:
      # Calculate mAP of predicted bboxes.

      def __init__(self, anno_json, classes, num_classes, min_score, nms_threshold, max_boxes):
          self.num_classes = num_classes
          self.classes = classes
          self.min_score = min_score
          self.nms_threshold = nms_threshold
          self.max_boxes = max_boxes

          self.val_cls_dict = {i: cls for i, cls in enumerate(classes)}
          self.coco_gt = COCO(anno_json)
          cat_ids = self.coco_gt.loadCats(self.coco_gt.getCatIds())
          self.class_dict = {cat['name']: cat['id'] for cat in cat_ids}

          self.predictions = []
          self.img_ids = []

      def update(self, batch):
          pred_boxes = batch['boxes']
          box_scores = batch['box_scores']
          img_id = batch['img_id']
          h, w = batch['image_shape']

          final_boxes = []
          final_label = []
          final_score = []
          self.img_ids.append(img_id)

          for c in range(1, self.num_classes):
              class_box_scores = box_scores[:, c]
              score_mask = class_box_scores > self.min_score
              class_box_scores = class_box_scores[score_mask]
              class_boxes = pred_boxes[score_mask] * [h, w, h, w]

              if score_mask.any():
                  nms_index = apply_nms(class_boxes, class_box_scores, self.nms_threshold, self.max_boxes)
                  class_boxes = class_boxes[nms_index]
                  class_box_scores = class_box_scores[nms_index]

                  final_boxes += class_boxes.tolist()
                  final_score += class_box_scores.tolist()
                  final_label += [self.class_dict[self.val_cls_dict[c]]] * len(class_box_scores)

          for loc, label, score in zip(final_boxes, final_label, final_score):
              res = {}
              res['image_id'] = img_id
              res['bbox'] = [loc[1], loc[0], loc[3] - loc[1], loc[2] - loc[0]]
              res['score'] = score
              res['category_id'] = label
              self.predictions.append(res)

      def get_metrics(self):
          with open('predictions.json', 'w') as f:
              json.dump(self.predictions, f)

          coco_dt = self.coco_gt.loadRes('predictions.json')
          E = COCOeval(self.coco_gt, coco_dt, iouType='bbox')
          E.params.imgIds = self.img_ids
          E.evaluate()
          E.accumulate()
          E.summarize()
          return E.stats[0]


  class SsdInferWithDecoder(nn.Cell):
      # SSD Infer wrapper to decode the bbox locations.

      def __init__(self, network, default_boxes, ckpt_path):
          super(SsdInferWithDecoder, self).__init__()
          param_dict = ms.load_checkpoint(ckpt_path)
          ms.load_param_into_net(network, param_dict)
          self.network = network
          self.default_boxes = default_boxes
          self.prior_scaling_xy = 0.1
          self.prior_scaling_wh = 0.2

      def construct(self, x):
          pred_loc, pred_label = self.network(x)

          default_bbox_xy = self.default_boxes[..., :2]
          default_bbox_wh = self.default_boxes[..., 2:]
          pred_xy = pred_loc[..., :2] * self.prior_scaling_xy * default_bbox_wh + default_bbox_xy
          pred_wh = ops.exp(pred_loc[..., 2:] * self.prior_scaling_wh) * default_bbox_wh

          pred_xy_0 = pred_xy - pred_wh / 2.0
          pred_xy_1 = pred_xy + pred_wh / 2.0
          pred_xy = ops.concat((pred_xy_0, pred_xy_1), -1)
          pred_xy = ops.maximum(pred_xy, 0)
          pred_xy = ops.minimum(pred_xy, 1)
          return pred_xy, pred_label

  import math
  import itertools as it

  from mindspore import set_seed

  class GeneratDefaultBoxes():
      # Generate Default boxes for SSD, follows the order of (W, H, archor_sizes).
      # `self.default_boxes` has a shape of [archor_sizes, H, W, 4], the last dimension is [y, x, h, w].
      # `self.default_boxes_tlbr` has a shape as `self.default_boxes`, the last dimension is [y1, x1, y2, x2].

      def __init__(self):
          fk = 300 / np.array([8, 16, 32, 64, 100, 300])
          scale_rate = (0.95 - 0.1) / (len([4, 6, 6, 6, 4, 4]) - 1)
          scales = [0.1 + scale_rate * i for i in range(len([4, 6, 6, 6, 4, 4]))] + [1.0]
          self.default_boxes = []
          for idex, feature_size in enumerate([38, 19, 10, 5, 3, 1]):
              sk1 = scales[idex]
              sk2 = scales[idex + 1]
              sk3 = math.sqrt(sk1 * sk2)
              if idex == 0 and not [[2], [2, 3], [2, 3], [2, 3], [2], [2]][idex]:
                  w, h = sk1 * math.sqrt(2), sk1 / math.sqrt(2)
                  all_sizes = [(0.1, 0.1), (w, h), (h, w)]
              else:
                  all_sizes = [(sk1, sk1)]
                  for aspect_ratio in [[2], [2, 3], [2, 3], [2, 3], [2], [2]][idex]:
                      w, h = sk1 * math.sqrt(aspect_ratio), sk1 / math.sqrt(aspect_ratio)
                      all_sizes.append((w, h))
                      all_sizes.append((h, w))
                  all_sizes.append((sk3, sk3))

              assert len(all_sizes) == [4, 6, 6, 6, 4, 4][idex]

              for i, j in it.product(range(feature_size), repeat=2):
                  for w, h in all_sizes:
                      cx, cy = (j + 0.5) / fk[idex], (i + 0.5) / fk[idex]
                      self.default_boxes.append([cy, cx, h, w])

          def to_tlbr(cy, cx, h, w):
              return cy - h / 2, cx - w / 2, cy + h / 2, cx + w / 2

          # For IoU calculation
          self.default_boxes_tlbr = np.array(tuple(to_tlbr(*i) for i in self.default_boxes), dtype='float32')
          self.default_boxes = np.array(self.default_boxes, dtype='float32')

  default_boxes_tlbr = GeneratDefaultBoxes().default_boxes_tlbr
  default_boxes = GeneratDefaultBoxes().default_boxes

  y1, x1, y2, x2 = np.split(default_boxes_tlbr[:, :4], 4, axis=-1)
  vol_anchors = (x2 - x1) * (y2 - y1)
  matching_threshold = 0.5

  from mindspore.common.initializer import initializer, TruncatedNormal


  def init_net_param(network, initialize_mode='TruncatedNormal'):
      # Init the parameters in net.
      params = network.trainable_params()
      for p in params:
          if 'beta' not in p.name and 'gamma' not in p.name and 'bias' not in p.name:
              if initialize_mode == 'TruncatedNormal':
                  p.set_data(initializer(TruncatedNormal(0.02), p.data.shape, p.data.dtype))
              else:
                  p.set_data(initialize_mode, p.data.shape, p.data.dtype)


  def get_lr(global_step, lr_init, lr_end, lr_max, warmup_epochs, total_epochs, steps_per_epoch):
      # generate learning rate array
      lr_each_step = []
      total_steps = steps_per_epoch * total_epochs
      warmup_steps = steps_per_epoch * warmup_epochs
      for i in range(total_steps):
          if i < warmup_steps:
              lr = lr_init + (lr_max - lr_init) * i / warmup_steps
          else:
              lr = lr_end + (lr_max - lr_end) * (1. + math.cos(math.pi * (i - warmup_steps) / (total_steps - warmup_steps))) / 2.
          if lr < 0.0:
              lr = 0.0
          lr_each_step.append(lr)

      current_step = global_step
      lr_each_step = np.array(lr_each_step).astype(np.float32)
      learning_rate = lr_each_step[current_step:]

      return learning_rate

  import time

  from mindspore.amp import DynamicLossScaler

  set_seed(1)

  # load data
  mindrecord_dir = "./datasets/MindRecord_COCO"
  mindrecord_file = "./datasets/MindRecord_COCO/ssd.mindrecord0"

  dataset = create_ssd_dataset(mindrecord_file, batch_size=5, rank=0, use_multiprocessing=True)
  dataset_size = dataset.get_dataset_size()

  image, get_loc, gt_label, num_matched_boxes = next(dataset.create_tuple_iterator())

  # Network definition and initialization
  network = SSD300Vgg16()
  init_net_param(network)

  # Define the learning rate
  lr = Tensor(get_lr(global_step=0 * dataset_size,
                    lr_init=0.001, lr_end=0.001 * 0.05, lr_max=0.05,
                    warmup_epochs=2, total_epochs=60, steps_per_epoch=dataset_size))

  # Define the optimizer
  opt = nn.Momentum(filter(lambda x: x.requires_grad, network.get_parameters()), lr,
                    0.9, 0.00015, float(1024))

  # Define the forward procedure
  def forward_fn(x, gt_loc, gt_label, num_matched_boxes):
      pred_loc, pred_label = network(x)
      mask = ops.less(0, gt_label).astype(ms.float32)
      num_matched_boxes = ops.sum(num_matched_boxes.astype(ms.float32))

      # Positioning loss
      mask_loc = ops.tile(ops.expand_dims(mask, -1), (1, 1, 4))
      smooth_l1 = nn.SmoothL1Loss()(pred_loc, gt_loc) * mask_loc
      loss_loc = ops.sum(ops.sum(smooth_l1, -1), -1)

      # Category loss
      loss_cls = class_loss(pred_label, gt_label)
      loss_cls = ops.sum(loss_cls, (1, 2))

      return ops.sum((loss_cls + loss_loc) / num_matched_boxes)

  grad_fn = ms.value_and_grad(forward_fn, None, opt.parameters, has_aux=False)
  loss_scaler = DynamicLossScaler(1024, 2, 1000)

  # Gradient updates
  def train_step(x, gt_loc, gt_label, num_matched_boxes):
      loss, grads = grad_fn(x, gt_loc, gt_label, num_matched_boxes)
      opt(grads)
      return loss

  print("=================== Starting Training =====================")
  iterator = dataset.create_tuple_iterator(num_epochs=60)
  for epoch in range(60):
      network.set_train(True)
      begin_time = time.time()
      for step, (image, get_loc, gt_label, num_matched_boxes) in enumerate(iterator):
          loss = train_step(image, get_loc, gt_label, num_matched_boxes)
      end_time = time.time()
      times = end_time - begin_time
      print(f"Epoch:[{int(epoch + 1)}/{int(60)}], "
            f"loss:{loss} , "
            f"time:{times}s ")
  ms.save_checkpoint(network, "ssd-60_9.ckpt")
  print("=================== Training Success =====================")

  mindrecord_file = "./datasets/MindRecord_COCO/ssd_eval.mindrecord0"

  def ssd_eval(dataset_path, ckpt_path, anno_json):
      # SSD evaluation.
      batch_size = 1
      ds = create_ssd_dataset(dataset_path, batch_size=batch_size,
                              is_training=False, use_multiprocessing=False)

      network = SSD300Vgg16()
      print("Load Checkpoint!")
      net = SsdInferWithDecoder(network, Tensor(default_boxes), ckpt_path)

      net.set_train(False)
      total = ds.get_dataset_size() * batch_size
      print("\n========================================\n")
      print("total images num: ", total)
      eval_param_dict = {"net": net, "dataset": ds, "anno_json": anno_json}
      mAP = apply_eval(eval_param_dict)
      print("\n========================================\n")
      print(f"mAP: {mAP}")

  def eval_net():
      print("Start Eval!")
      ssd_eval(mindrecord_file, "./ssd-60_9.ckpt", anno_json)

  eval_net()
  """
  print(sddite)

# 
def vision_transformer():
  vt = """
  from download import download

  dataset_url = "https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/notebook/datasets/vit_imagenet_dataset.zip"
  path = "./"

  path = download(dataset_url, path, kind="zip", replace=True)

  import os

  import mindspore as ms
  from mindspore.dataset import ImageFolderDataset
  import mindspore.dataset.vision as transforms


  data_path = './dataset/'
  mean = [0.485 * 255, 0.456 * 255, 0.406 * 255]
  std = [0.229 * 255, 0.224 * 255, 0.225 * 255]

  dataset_train = ImageFolderDataset(os.path.join(data_path, "train"), shuffle=True)

  trans_train = [
      transforms.RandomCropDecodeResize(size=224,
                                        scale=(0.08, 1.0),
                                        ratio=(0.75, 1.333)),
      transforms.RandomHorizontalFlip(prob=0.5),
      transforms.Normalize(mean=mean, std=std),
      transforms.HWC2CHW()
  ]

  dataset_train = dataset_train.map(operations=trans_train, input_columns=["image"])
  dataset_train = dataset_train.batch(batch_size=16, drop_remainder=True)

  from mindspore import nn, ops


  class Attention(nn.Cell):
      def __init__(self,
                  dim: int,
                  num_heads: int = 8,
                  keep_prob: float = 1.0,
                  attention_keep_prob: float = 1.0):
          super(Attention, self).__init__()

          self.num_heads = num_heads
          head_dim = dim // num_heads
          self.scale = ms.Tensor(head_dim ** -0.5)

          self.qkv = nn.Dense(dim, dim * 3)
          self.attn_drop = nn.Dropout(p=1.0-attention_keep_prob)
          self.out = nn.Dense(dim, dim)
          self.out_drop = nn.Dropout(p=1.0-keep_prob)
          self.attn_matmul_v = ops.BatchMatMul()
          self.q_matmul_k = ops.BatchMatMul(transpose_b=True)
          self.softmax = nn.Softmax(axis=-1)

      def construct(self, x):
          # Attention construct.
          b, n, c = x.shape
          qkv = self.qkv(x)
          qkv = ops.reshape(qkv, (b, n, 3, self.num_heads, c // self.num_heads))
          qkv = ops.transpose(qkv, (2, 0, 3, 1, 4))
          q, k, v = ops.unstack(qkv, axis=0)
          attn = self.q_matmul_k(q, k)
          attn = ops.mul(attn, self.scale)
          attn = self.softmax(attn)
          attn = self.attn_drop(attn)
          out = self.attn_matmul_v(attn, v)
          out = ops.transpose(out, (0, 2, 1, 3))
          out = ops.reshape(out, (b, n, c))
          out = self.out(out)
          out = self.out_drop(out)

          return out

  from typing import Optional, Dict


  class FeedForward(nn.Cell):
      def __init__(self,
                  in_features: int,
                  hidden_features: Optional[int] = None,
                  out_features: Optional[int] = None,
                  activation: nn.Cell = nn.GELU,
                  keep_prob: float = 1.0):
          super(FeedForward, self).__init__()
          out_features = out_features or in_features
          hidden_features = hidden_features or in_features
          self.dense1 = nn.Dense(in_features, hidden_features)
          self.activation = activation()
          self.dense2 = nn.Dense(hidden_features, out_features)
          self.dropout = nn.Dropout(p=1.0-keep_prob)

      def construct(self, x):
          # Feed Forward construct.
          x = self.dense1(x)
          x = self.activation(x)
          x = self.dropout(x)
          x = self.dense2(x)
          x = self.dropout(x)

          return x


  class ResidualCell(nn.Cell):
      def __init__(self, cell):
          super(ResidualCell, self).__init__()
          self.cell = cell

      def construct(self, x):
          # ResidualCell construct.
          return self.cell(x) + x

  class TransformerEncoder(nn.Cell):
      def __init__(self,
                  dim: int,
                  num_layers: int,
                  num_heads: int,
                  mlp_dim: int,
                  keep_prob: float = 1.,
                  attention_keep_prob: float = 1.0,
                  drop_path_keep_prob: float = 1.0,
                  activation: nn.Cell = nn.GELU,
                  norm: nn.Cell = nn.LayerNorm):
          super(TransformerEncoder, self).__init__()
          layers = []

          for _ in range(num_layers):
              normalization1 = norm((dim,))
              normalization2 = norm((dim,))
              attention = Attention(dim=dim,
                                    num_heads=num_heads,
                                    keep_prob=keep_prob,
                                    attention_keep_prob=attention_keep_prob)

              feedforward = FeedForward(in_features=dim,
                                        hidden_features=mlp_dim,
                                        activation=activation,
                                        keep_prob=keep_prob)

              layers.append(
                  nn.SequentialCell([
                      ResidualCell(nn.SequentialCell([normalization1, attention])),
                      ResidualCell(nn.SequentialCell([normalization2, feedforward]))
                  ])
              )
          self.layers = nn.SequentialCell(layers)

      def construct(self, x):
          # Transformer construct.
          return self.layers(x)

  class PatchEmbedding(nn.Cell):
      MIN_NUM_PATCHES = 4

      def __init__(self,
                  image_size: int = 224,
                  patch_size: int = 16,
                  embed_dim: int = 768,
                  input_channels: int = 3):
          super(PatchEmbedding, self).__init__()

          self.image_size = image_size
          self.patch_size = patch_size
          self.num_patches = (image_size // patch_size) ** 2
          self.conv = nn.Conv2d(input_channels, embed_dim, kernel_size=patch_size, stride=patch_size, has_bias=True)

      def construct(self, x):
          # Path Embedding construct.
          x = self.conv(x)
          b, c, h, w = x.shape
          x = ops.reshape(x, (b, c, h * w))
          x = ops.transpose(x, (0, 2, 1))

          return x

  from mindspore.common.initializer import Normal
  from mindspore.common.initializer import initializer
  from mindspore import Parameter


  def init(init_type, shape, dtype, name, requires_grad):
      # Init.
      initial = initializer(init_type, shape, dtype).init_data()
      return Parameter(initial, name=name, requires_grad=requires_grad)


  class ViT(nn.Cell):
      def __init__(self,
                  image_size: int = 224,
                  input_channels: int = 3,
                  patch_size: int = 16,
                  embed_dim: int = 768,
                  num_layers: int = 12,
                  num_heads: int = 12,
                  mlp_dim: int = 3072,
                  keep_prob: float = 1.0,
                  attention_keep_prob: float = 1.0,
                  drop_path_keep_prob: float = 1.0,
                  activation: nn.Cell = nn.GELU,
                  norm: Optional[nn.Cell] = nn.LayerNorm,
                  pool: str = 'cls') -> None:
          super(ViT, self).__init__()

          self.patch_embedding = PatchEmbedding(image_size=image_size,
                                                patch_size=patch_size,
                                                embed_dim=embed_dim,
                                                input_channels=input_channels)
          num_patches = self.patch_embedding.num_patches

          self.cls_token = init(init_type=Normal(sigma=1.0),
                                shape=(1, 1, embed_dim),
                                dtype=ms.float32,
                                name='cls',
                                requires_grad=True)

          self.pos_embedding = init(init_type=Normal(sigma=1.0),
                                    shape=(1, num_patches + 1, embed_dim),
                                    dtype=ms.float32,
                                    name='pos_embedding',
                                    requires_grad=True)

          self.pool = pool
          self.pos_dropout = nn.Dropout(p=1.0-keep_prob)
          self.norm = norm((embed_dim,))
          self.transformer = TransformerEncoder(dim=embed_dim,
                                                num_layers=num_layers,
                                                num_heads=num_heads,
                                                mlp_dim=mlp_dim,
                                                keep_prob=keep_prob,
                                                attention_keep_prob=attention_keep_prob,
                                                drop_path_keep_prob=drop_path_keep_prob,
                                                activation=activation,
                                                norm=norm)
          self.dropout = nn.Dropout(p=1.0-keep_prob)
          self.dense = nn.Dense(embed_dim, num_classes)

      def construct(self, x):
          # ViT construct.
          x = self.patch_embedding(x)
          cls_tokens = ops.tile(self.cls_token.astype(x.dtype), (x.shape[0], 1, 1))
          x = ops.concat((cls_tokens, x), axis=1)
          x += self.pos_embedding

          x = self.pos_dropout(x)
          x = self.transformer(x)
          x = self.norm(x)
          x = x[:, 0]
          if self.training:
              x = self.dropout(x)
          x = self.dense(x)

          return x

  from mindspore.nn import LossBase
  from mindspore.train import LossMonitor, TimeMonitor, CheckpointConfig, ModelCheckpoint
  from mindspore import train

  # define super parameter
  epoch_size = 10
  momentum = 0.9
  num_classes = 1000
  resize = 224
  step_size = dataset_train.get_dataset_size()

  # construct model
  network = ViT()

  # load ckpt
  vit_url = "https://download.mindspore.cn/vision/classification/vit_b_16_224.ckpt"
  path = "./ckpt/vit_b_16_224.ckpt"

  vit_path = download(vit_url, path, replace=True)
  param_dict = ms.load_checkpoint(vit_path)
  ms.load_param_into_net(network, param_dict)

  # define learning rate
  lr = nn.cosine_decay_lr(min_lr=float(0),
                          max_lr=0.00005,
                          total_step=epoch_size * step_size,
                          step_per_epoch=step_size,
                          decay_epoch=10)

  # define optimizer
  network_opt = nn.Adam(network.trainable_params(), lr, momentum)


  # define loss function
  class CrossEntropySmooth(LossBase):
      # CrossEntropy.

      def __init__(self, sparse=True, reduction='mean', smooth_factor=0., num_classes=1000):
          super(CrossEntropySmooth, self).__init__()
          self.onehot = ops.OneHot()
          self.sparse = sparse
          self.on_value = ms.Tensor(1.0 - smooth_factor, ms.float32)
          self.off_value = ms.Tensor(1.0 * smooth_factor / (num_classes - 1), ms.float32)
          self.ce = nn.SoftmaxCrossEntropyWithLogits(reduction=reduction)

      def construct(self, logit, label):
          if self.sparse:
              label = self.onehot(label, ops.shape(logit)[1], self.on_value, self.off_value)
          loss = self.ce(logit, label)
          return loss


  network_loss = CrossEntropySmooth(sparse=True,
                                    reduction="mean",
                                    smooth_factor=0.1,
                                    num_classes=num_classes)

  # set checkpoint
  ckpt_config = CheckpointConfig(save_checkpoint_steps=step_size, keep_checkpoint_max=100)
  ckpt_callback = ModelCheckpoint(prefix='vit_b_16', directory='./ViT', config=ckpt_config)

  # initialize model
  # "Ascend + mixed precision" can improve performance
  ascend_target = (ms.get_context("device_target") == "Ascend")
  if ascend_target:
      model = train.Model(network, loss_fn=network_loss, optimizer=network_opt, metrics={"acc"}, amp_level="O2")
  else:
      model = train.Model(network, loss_fn=network_loss, optimizer=network_opt, metrics={"acc"}, amp_level="O0")

  # train model
  model.train(epoch_size,
              dataset_train,
              callbacks=[ckpt_callback, LossMonitor(125), TimeMonitor(125)],
              dataset_sink_mode=False,)

  dataset_val = ImageFolderDataset(os.path.join(data_path, "val"), shuffle=True)

  trans_val = [
      transforms.Decode(),
      transforms.Resize(224 + 32),
      transforms.CenterCrop(224),
      transforms.Normalize(mean=mean, std=std),
      transforms.HWC2CHW()
  ]

  dataset_val = dataset_val.map(operations=trans_val, input_columns=["image"])
  dataset_val = dataset_val.batch(batch_size=16, drop_remainder=True)

  # construct model
  network = ViT()

  # load ckpt
  param_dict = ms.load_checkpoint(vit_path)
  ms.load_param_into_net(network, param_dict)

  network_loss = CrossEntropySmooth(sparse=True,
                                    reduction="mean",
                                    smooth_factor=0.1,
                                    num_classes=num_classes)

  # define metric
  eval_metrics = {'Top_1_Accuracy': train.Top1CategoricalAccuracy(),
                  'Top_5_Accuracy': train.Top5CategoricalAccuracy()}

  if ascend_target:
      model = train.Model(network, loss_fn=network_loss, optimizer=network_opt, metrics=eval_metrics, amp_level="O2")
  else:
      model = train.Model(network, loss_fn=network_loss, optimizer=network_opt, metrics=eval_metrics, amp_level="O0")

  # evaluate model
  result = model.eval(dataset_val)
  print(result)

  dataset_infer = ImageFolderDataset(os.path.join(data_path, "infer"), shuffle=True)

  trans_infer = [
      transforms.Decode(),
      transforms.Resize([224, 224]),
      transforms.Normalize(mean=mean, std=std),
      transforms.HWC2CHW()
  ]

  dataset_infer = dataset_infer.map(operations=trans_infer,
                                    input_columns=["image"],
                                    num_parallel_workers=1)
  dataset_infer = dataset_infer.batch(1)

  import os
  import pathlib
  import cv2
  import numpy as np
  from PIL import Image
  from enum import Enum
  from scipy import io


  class Color(Enum):
      # dedine enum color.
      red = (0, 0, 255)
      green = (0, 255, 0)
      blue = (255, 0, 0)
      cyan = (255, 255, 0)
      yellow = (0, 255, 255)
      magenta = (255, 0, 255)
      white = (255, 255, 255)
      black = (0, 0, 0)


  def check_file_exist(file_name: str):
      # check_file_exist.
      if not os.path.isfile(file_name):
          raise FileNotFoundError(f"File `{file_name}` does not exist.")


  def color_val(color):
      # color_val.
      if isinstance(color, str):
          return Color[color].value
      if isinstance(color, Color):
          return color.value
      if isinstance(color, tuple):
          assert len(color) == 3
          for channel in color:
              assert 0 <= channel <= 255
          return color
      if isinstance(color, int):
          assert 0 <= color <= 255
          return color, color, color
      if isinstance(color, np.ndarray):
          assert color.ndim == 1 and color.size == 3
          assert np.all((color >= 0) & (color <= 255))
          color = color.astype(np.uint8)
          return tuple(color)
      raise TypeError(f'Invalid type for color: {type(color)}')


  def imread(image, mode=None):
      # imread.
      if isinstance(image, pathlib.Path):
          image = str(image)

      if isinstance(image, np.ndarray):
          pass
      elif isinstance(image, str):
          check_file_exist(image)
          image = Image.open(image)
          if mode:
              image = np.array(image.convert(mode))
      else:
          raise TypeError("Image must be a `ndarray`, `str` or Path object.")

      return image


  def imwrite(image, image_path, auto_mkdir=True):
      if auto_mkdir:
          dir_name = os.path.abspath(os.path.dirname(image_path))
          if dir_name != '':
              dir_name = os.path.expanduser(dir_name)
              os.makedirs(dir_name, mode=777, exist_ok=True)

      image = Image.fromarray(image)
      image.save(image_path)


  def imshow(img, win_name='', wait_time=0):
      cv2.imshow(win_name, imread(img))
      if wait_time == 0:  # prevent from hanging if windows was closed
          while True:
              ret = cv2.waitKey(1)

              closed = cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) < 1
              # if user closed window or if some key pressed
              if closed or ret != -1:
                  break
      else:
          ret = cv2.waitKey(wait_time)


  def show_result(img: str,
                  result: Dict[int, float],
                  text_color: str = 'green',
                  font_scale: float = 0.5,
                  row_width: int = 20,
                  show: bool = False,
                  win_name: str = '',
                  wait_time: int = 0,
                  out_file: Optional[str] = None) -> None:
      img = imread(img, mode="RGB")
      img = img.copy()
      x, y = 0, row_width
      text_color = color_val(text_color)
      for k, v in result.items():
          if isinstance(v, float):
              v = f'{v:.2f}'
          label_text = f'{k}: {v}'
          cv2.putText(img, label_text, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                      font_scale, text_color)
          y += row_width
      if out_file:
          show = False
          imwrite(img, out_file)

      if show:
          imshow(img, win_name, wait_time)


  def index2label():
      # Dictionary output for image numbers and categories of the ImageNet dataset.
      metafile = os.path.join(data_path, "ILSVRC2012_devkit_t12/data/meta.mat")
      meta = io.loadmat(metafile, squeeze_me=True)['synsets']

      nums_children = list(zip(*meta))[4]
      meta = [meta[idx] for idx, num_children in enumerate(nums_children) if num_children == 0]

      _, wnids, classes = list(zip(*meta))[:3]
      clssname = [tuple(clss.split(', ')) for clss in classes]
      wnid2class = {wnid: clss for wnid, clss in zip(wnids, clssname)}
      wind2class_name = sorted(wnid2class.items(), key=lambda x: x[0])

      mapping = {}
      for index, (_, class_name) in enumerate(wind2class_name):
          mapping[index] = class_name[0]
      return mapping


  # Read data for inference
  for i, image in enumerate(dataset_infer.create_dict_iterator(output_numpy=True)):
      image = image["image"]
      image = ms.Tensor(image)
      prob = model.predict(image)
      label = np.argmax(prob.asnumpy(), axis=1)
      mapping = index2label()
      output = {int(label): mapping[int(label)]}
      print(output)
      show_result(img="./dataset/infer/n01440764/ILSVRC2012_test_00000279.JPEG",
                  result=output,
                  out_file="./dataset/infer/ILSVRC2012_test_00000279.JPEG")
  """
  print(vt)

#
def lstm_crf():
  lstmcrf = """
  def compute_score(emissions, tags, seq_ends, mask, trans, start_trans, end_trans):
      # emissions: (seq_length, batch_size, num_tags)
      # tags: (seq_length, batch_size)
      # mask: (seq_length, batch_size)

      seq_length, batch_size = tags.shape
      mask = mask.astype(emissions.dtype)

      # Set score to the initial transition probability.
      # shape: (batch_size,)
      score = start_trans[tags[0]]
      # score += Probability of the first emission
      # shape: (batch_size,)
      score += emissions[0, mnp.arange(batch_size), tags[0]]

      for i in range(1, seq_length):
          # Probability that the label is transited from i-1 to i (valid when mask == 1).
          # shape: (batch_size,)
          score += trans[tags[i - 1], tags[i]] * mask[i]

          # Emission probability of tags[i] prediction(valid when mask == 1).
          # shape: (batch_size,)
          score += emissions[i, mnp.arange(batch_size), tags[i]] * mask[i]

      # End the transition.
      # shape: (batch_size,)
      last_tags = tags[seq_ends, mnp.arange(batch_size)]
      # score += End transition probability
      # shape: (batch_size,)
      score += end_trans[last_tags]

      return score

  def compute_normalizer(emissions, mask, trans, start_trans, end_trans):
      # emissions: (seq_length, batch_size, num_tags)
      # mask: (seq_length, batch_size)

      seq_length = emissions.shape[0]

      # Set score to the initial transition probability and add the first emission probability.
      # shape: (batch_size, num_tags)
      score = start_trans + emissions[0]

      for i in range(1, seq_length):
          # The score dimension is extended to calculate the total score.
          # shape: (batch_size, num_tags, 1)
          broadcast_score = score.expand_dims(2)

          # The emission dimension is extended to calculate the total score.
          # shape: (batch_size, 1, num_tags)
          broadcast_emissions = emissions[i].expand_dims(1)

          # Calculate score_i according to formula (7).
          # In this case, broadcast_score indicates all possible paths from token 0 to the current token.
          # log_sum_exp corresponding to score
          # shape: (batch_size, num_tags, num_tags)
          next_score = broadcast_score + trans + broadcast_emissions

          # Perform the log_sum_exp operation on score_i to calculate the score of the next token.
          # shape: (batch_size, num_tags)
          next_score = ops.logsumexp(next_score, dim=1)

          # The score changes only when mask == 1.
          # shape: (batch_size, num_tags)
          score = mnp.where(mask[i].expand_dims(1), next_score, score)

      # Add the end transition probability.
      # shape: (batch_size, num_tags)
      score += end_trans
      # Calculate log_sum_exp based on the scores of all possible paths.
      # shape: (batch_size,)
      return ops.logsumexp(score, dim=1)

  def viterbi_decode(emissions, mask, trans, start_trans, end_trans):
      # emissions: (seq_length, batch_size, num_tags)
      # mask: (seq_length, batch_size)

      seq_length = mask.shape[0]

      score = start_trans + emissions[0]
      history = ()

      for i in range(1, seq_length):
          broadcast_score = score.expand_dims(2)
          broadcast_emission = emissions[i].expand_dims(1)
          next_score = broadcast_score + trans + broadcast_emission

          # Obtain the label with the maximum score corresponding to the current token and save the label.
          indices = next_score.argmax(axis=1)
          history += (indices,)

          next_score = next_score.max(axis=1)
          score = mnp.where(mask[i].expand_dims(1), next_score, score)

      score += end_trans

      return score, history

  def post_decode(score, history, seq_length):
      # Use Score and History to calculate the optimal prediction sequence.
      batch_size = seq_length.shape[0]
      seq_ends = seq_length - 1
      # shape: (batch_size,)
      best_tags_list = []

      # Decode each sample in a batch in sequence.
      for idx in range(batch_size):
          # Search for the label that maximizes the prediction probability corresponding to the last token.
          # Add it to the list of best prediction sequence stores.
          best_last_tag = score[idx].argmax(axis=0)
          best_tags = [int(best_last_tag.asnumpy())]

          # Repeatedly search for the label with the maximum prediction probability corresponding to each token and add the label to the list.
          for hist in reversed(history[:seq_ends[idx]]):
              best_last_tag = hist[idx][best_tags[-1]]
              best_tags.append(int(best_last_tag.asnumpy()))

          # Reset the solved label sequence in reverse order to the positive sequence.
          best_tags.reverse()
          best_tags_list.append(best_tags)

      return best_tags_list

  import mindspore as ms
  import mindspore.nn as nn
  import mindspore.ops as ops
  import mindspore.numpy as mnp
  from mindspore.common.initializer import initializer, Uniform

  def sequence_mask(seq_length, max_length, batch_first=False):
      # Generate the mask matrix based on the actual length and maximum length of the sequence.
      range_vector = mnp.arange(0, max_length, 1, seq_length.dtype)
      result = range_vector < seq_length.view(seq_length.shape + (1,))
      if batch_first:
          return result.astype(ms.int64)
      return result.astype(ms.int64).swapaxes(0, 1)

  class CRF(nn.Cell):
      def __init__(self, num_tags: int, batch_first: bool = False, reduction: str = 'sum') -> None:
          if num_tags <= 0:
              raise ValueError(f'invalid number of tags: {num_tags}')
          super().__init__()
          if reduction not in ('none', 'sum', 'mean', 'token_mean'):
              raise ValueError(f'invalid reduction: {reduction}')
          self.num_tags = num_tags
          self.batch_first = batch_first
          self.reduction = reduction
          self.start_transitions = ms.Parameter(initializer(Uniform(0.1), (num_tags,)), name='start_transitions')
          self.end_transitions = ms.Parameter(initializer(Uniform(0.1), (num_tags,)), name='end_transitions')
          self.transitions = ms.Parameter(initializer(Uniform(0.1), (num_tags, num_tags)), name='transitions')

      def construct(self, emissions, tags=None, seq_length=None):
          if tags is None:
              return self._decode(emissions, seq_length)
          return self._forward(emissions, tags, seq_length)

      def _forward(self, emissions, tags=None, seq_length=None):
          if self.batch_first:
              batch_size, max_length = tags.shape
              emissions = emissions.swapaxes(0, 1)
              tags = tags.swapaxes(0, 1)
          else:
              max_length, batch_size = tags.shape

          if seq_length is None:
              seq_length = mnp.full((batch_size,), max_length, ms.int64)

          mask = sequence_mask(seq_length, max_length)

          # shape: (batch_size,)
          numerator = compute_score(emissions, tags, seq_length-1, mask, self.transitions, self.start_transitions, self.end_transitions)
          # shape: (batch_size,)
          denominator = compute_normalizer(emissions, mask, self.transitions, self.start_transitions, self.end_transitions)
          # shape: (batch_size,)
          llh = denominator - numerator

          if self.reduction == 'none':
              return llh
          if self.reduction == 'sum':
              return llh.sum()
          if self.reduction == 'mean':
              return llh.mean()
          return llh.sum() / mask.astype(emissions.dtype).sum()

      def _decode(self, emissions, seq_length=None):
          if self.batch_first:
              batch_size, max_length = emissions.shape[:2]
              emissions = emissions.swapaxes(0, 1)
          else:
              batch_size, max_length = emissions.shape[:2]

          if seq_length is None:
              seq_length = mnp.full((batch_size,), max_length, ms.int64)

          mask = sequence_mask(seq_length, max_length)

          return viterbi_decode(emissions, mask, self.transitions, self.start_transitions, self.end_transitions)

  class BiLSTM_CRF(nn.Cell):
      def __init__(self, vocab_size, embedding_dim, hidden_dim, num_tags, padding_idx=0):
          super().__init__()
          self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
          self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2, bidirectional=True, batch_first=True)
          self.hidden2tag = nn.Dense(hidden_dim, num_tags, 'he_uniform')
          self.crf = CRF(num_tags, batch_first=True)

      def construct(self, inputs, seq_length, tags=None):
          embeds = self.embedding(inputs)
          outputs, _ = self.lstm(embeds, seq_length=seq_length)
          feats = self.hidden2tag(outputs)

          crf_outs = self.crf(feats, tags, seq_length)
          return crf_outs

  embedding_dim = 16
  hidden_dim = 32

  training_data = [(
      "the wall street journal reported today that apple corporation made money".split(),
      "B I I I O O O B I O O".split()
  ), (
      "georgia tech is a university in georgia".split(),
      "B I O O O O B".split()
  )]

  word_to_idx = {}
  word_to_idx['<pad>'] = 0
  for sentence, tags in training_data:
      for word in sentence:
          if word not in word_to_idx:
              word_to_idx[word] = len(word_to_idx)

  tag_to_idx = {"B": 0, "I": 1, "O": 2}

  len(word_to_idx)

  model = BiLSTM_CRF(len(word_to_idx), embedding_dim, hidden_dim, len(tag_to_idx))
  optimizer = nn.SGD(model.trainable_params(), learning_rate=0.01, weight_decay=1e-4)

  grad_fn = ms.value_and_grad(model, None, optimizer.parameters)

  def train_step(data, seq_length, label):
      loss, grads = grad_fn(data, seq_length, label)
      optimizer(grads)
      return loss

  def prepare_sequence(seqs, word_to_idx, tag_to_idx):
      seq_outputs, label_outputs, seq_length = [], [], []
      max_len = max([len(i[0]) for i in seqs])

      for seq, tag in seqs:
          seq_length.append(len(seq))
          idxs = [word_to_idx[w] for w in seq]
          labels = [tag_to_idx[t] for t in tag]
          idxs.extend([word_to_idx['<pad>'] for i in range(max_len - len(seq))])
          labels.extend([tag_to_idx['O'] for i in range(max_len - len(seq))])
          seq_outputs.append(idxs)
          label_outputs.append(labels)

      return ms.Tensor(seq_outputs, ms.int64), \
              ms.Tensor(label_outputs, ms.int64), \
              ms.Tensor(seq_length, ms.int64)

  data, label, seq_length = prepare_sequence(training_data, word_to_idx, tag_to_idx)
  data.shape, label.shape, seq_length.shape

  from tqdm import tqdm

  steps = 500
  with tqdm(total=steps) as t:
      for i in range(steps):
          loss = train_step(data, seq_length, label)
          t.set_postfix(loss=loss)
          t.update(1)

  score, history = model(data, seq_length)
  score

  predict = post_decode(score, history, seq_length)
  predict

  idx_to_tag = {idx: tag for tag, idx in tag_to_idx.items()}

  def sequence_to_tag(sequences, idx_to_tag):
      outputs = []
      for seq in sequences:
          outputs.append([idx_to_tag[i] for i in seq])
      return outputs

  sequence_to_tag(predict, idx_to_tag)
  """
  print(lstmcrf)