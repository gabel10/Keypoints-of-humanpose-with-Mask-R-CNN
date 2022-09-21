# Use the maskrcnn for the humanpose keypoints detection
mask rcnn can be used to the human keypoints detection


# Requirements

1、	Python3，Keras，TensorFlow。

 -   Python 3.4+
 -   TensorFlow 1.3+
 -   Keras 2.0.8+
 -   Jupyter Notebook
 -   Numpy, skimage, scipy, Pillow, cython, h5py
 -   opencv 2.0


2、MS COCO Requirements:

To train or test on MS COCO, you'll also need:

 -   pycocotools (installation instructions below)
 -   [MS COCO Dataset](http://cocodataset.org/#home)
 -   Download the 5K  [minival](https://dl.dropboxusercontent.com/s/o43o90bna78omob/instances_minival2014.json.zip?dl=0)  and the 35K  [validation-minus-minival](https://dl.dropboxusercontent.com/s/s3tw5zcg7395368/instances_valminusminival2014.json.zip?dl=0)  subsets. More details in the original  [Faster R-CNN implementation](https://github.com/rbgirshick/py-faster-rcnn/blob/master/data/README.md).
 
3、Download pre-trained COCO weights (mask_rcnn_coco_humanpose.h5) from the release page
4、(Optional) To train or test on MS COCO install  `pycocotools`  from one of these repos. They are forks of the original pycocotools with fixes for Python3 and Windows (the official repo doesn't seem to be active anymore).

-   Linux:  [https://github.com/waleedka/coco](https://github.com/waleedka/coco)
-   Windows:  [https://github.com/philferriere/cocoapi](https://github.com/philferriere/cocoapi). You must have the Visual C++ 2015 build tools on your path (see the repo for additional details)
 
Vínculo del dataset en: https://drive.google.com/file/d/1MfH1d-jzAfn8mELrSpzbnPyWjcVTGqaL/view?usp=sharing
