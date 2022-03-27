import os
import numpy as np
import glob
import cv2
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf

image_types = ('.jpg', 'jpeg', '.png', '.svg')

class ImageData():
    def __init__(self):
        pass

    def read_data_from_dir(self, imagedir, grayscale=True, read_labels=False):
        image_files = list()
        for file_type in image_types:
            image_files.extend(glob.glob(os.path.join(imagedir, "**/*" + file_type), recursive=True))
        if len(image_files) == 0:
            return None
        images = []
        for each_image_file in image_files:
            if grayscale:
                img = cv2.imread(each_image_file, cv2.IMREAD_GRAYSCALE)
            else:
                img = cv2.imread(each_image_file)
            if img is not None:
                images.append(img)
        train_x = np.asarray(images)
        if read_labels:
            csv_files = glob.glob(os.path.join(imagedir, "**/*" + ".csv"), recursive=True)
            label_data = pd.read_csv(csv_files[-1])
            train_y = label_data.iloc[:,-1:].values
            return train_x, train_y
        else:
            return train_x

    def read_classification_data(self, datadir):
        train_x = list()
        train_y = list()
        for dp, dn, filenames in os.walk(datadir):
            if len(filenames) > 0:
                current_class_data = self.read_data_from_dir(dp)
                train_x.extend(current_class_data)
                train_y.extend([os.path.basename(dp)] * current_class_data.shape[0])
        if len(train_x) == 0:
            return None
        train_x = np.asarray(train_x)
        train_y = np.asarray(train_y)
        train_y_classes, train_y = np.unique(train_y, return_inverse=True)
        return train_x, (train_y_classes, train_y)

    def resize_images(self, images, new_shape):
        resized_images = []
        for each_image in images:
            resized_images.append(cv2.resize(each_image, new_shape, interpolation= cv2.INTER_LINEAR))
        resized_images = np.asarray(resized_images)
        return resized_images
        
        
imd = ImageData()
train_x, train_y = imd.read_classification_data("/data")
train_y_classes, train_y = train_y
resized_train_x = imd.resize_images(train_x, (200,200))
resized_train_x = resized_train_x.reshape(resized_train_x.shape[0], 200, 200, 1)

encoder = OneHotEncoder(sparse=False)
onehot = encoder.fit_transform(train_y.reshape(-1, 1))

model = tf.keras.models.Sequential([
  tf.keras.layers.InputLayer(input_shape=(200,200,1)),
  tf.keras.layers.Conv2D(2, 4, strides=2, padding='same', activation=tf.nn.relu),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(2)
])
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
              
model.fit(x=resized_train_x, y=onehot,epochs=6, verbose=True)
model.save("/model/1")