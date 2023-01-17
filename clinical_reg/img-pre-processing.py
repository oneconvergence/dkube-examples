import warnings
warnings.filterwarnings("ignore")

import cv2
import pydicom
import os, shutil
import tensorflow as tf
from matplotlib.pyplot import imshow

IMG_DIR = '/opt/dkube/input/'
OUT_DIR = '/opt/dkube/output/'
dim = (28,28)
raw_imgs_names = tf.io.gfile.listdir(IMG_DIR + 'imgs/')

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
for each_img in raw_imgs_names:
    fname = os.path.splitext(each_img)[0]
    fname = fname.split('/')[-1]
    ds = pydicom.dcmread(IMG_DIR + 'imgs/' + each_img)
    resized = cv2.resize(ds.pixel_array, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(OUT_DIR + fname + '.png',resized)
