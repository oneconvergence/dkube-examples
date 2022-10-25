#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time
import random
import string
from dkube.sdk import mlflow as dkubemlf

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report
import tensorflow as tf
import mlflow
import matplotlib.pyplot as plt

import requests
requests.packages.urllib3.disable_warnings()

import warnings
warnings.filterwarnings("ignore")

import sys
utildir = os.path.abspath('.')
if utildir not in sys.path:
    sys.path.insert(0, utildir)
import util


# ### MACROS

# In[2]:


# Define where the input data dir and model output dir are
INPUT_DATA_DIR = "/mnt/data"
OUTPUT_MODEL_DIR = "/mnt/model"
NUM_EPOCHS = os.getenv("EPOCHS", 6)
MLFLOW_EXPERIMENT_NAME = os.getenv("DKUBE_PROJECT_NAME", "default")
DKUBE_INPUT_CODE = "chest-xray"
DKUBE_INPUT_DATASET = "chest-xray"
DKUBE_OUTPUT_MODEL = "chest-xray"


# #### MLFLOW TRACKING INITIALIZATION

# In[3]:


import warnings
warnings.filterwarnings('ignore')
exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
if not exp:
    print("Creating experiment...")
    mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT_NAME)
mlflow.tensorflow.autolog(silent=True)


# In[4]:


train_x, train_y = util.read_classification_data(INPUT_DATA_DIR)
train_y_classes, train_y = train_y
resized_train_x = util.resize_images(train_x, (200,200))
resized_train_x = resized_train_x.reshape(resized_train_x.shape[0], 200, 200, 1)

encoder = OneHotEncoder(sparse=False)
onehot = encoder.fit_transform(train_y.reshape(-1, 1))

train_x, test_x, train_y, test_y = train_test_split(resized_train_x, onehot, test_size=0.2)

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


# #### ML TRAINING

# In[5]:


runid = dkubemlf.create_run(code=DKUBE_INPUT_CODE, dataset=DKUBE_INPUT_DATASET,output=DKUBE_OUTPUT_MODEL)


# In[6]:


with mlflow.start_run(run_id=runid) as run:
    model.fit(x=resized_train_x, y=onehot,epochs=NUM_EPOCHS, verbose=True)
    if os.getenv("DKUBE_JOB_CLASS") != "notebook" :
        model.save(f"{OUTPUT_MODEL_DIR}/1")

    mlflow.log_artifacts(OUTPUT_MODEL_DIR, artifact_path="saved_model")

    pred = model.predict(test_x.astype('float32'))
    predicted_class = train_y_classes[pred.argmax(axis=1)]
    test_labels = train_y_classes[test_y.argmax(axis=1)]
    cm = confusion_matrix(test_labels, predicted_class)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    time.sleep(1)
    plt.savefig("confusion-matrix.png")
    mlflow.log_artifact("confusion-matrix.png")

    cr = classification_report(test_labels, predicted_class, output_dict=True)
    print(cr)

    recall_0 = cr['NORMAL']['recall']
    f1_score_0 = cr['NORMAL']['f1-score']
    recall_1 = cr['PNEUMONIA']['recall']
    f1_score_1 = cr['PNEUMONIA']['f1-score']

    tp = cm[0][0]
    tn = cm[1][1]
    fp = cm[0][1]
    fn = cm[1][0]

    mlflow.log_metric("true_positive", tp)
    mlflow.log_metric("true_negative", tn)
    mlflow.log_metric("false_positive", fp)
    mlflow.log_metric("false_negative", fn)
    mlflow.log_metric("recall_NORMAL", recall_0)
    mlflow.log_metric("f1_score_NORMAL", f1_score_0)
    mlflow.log_metric("recall_PNEUMONIA", recall_1)
    mlflow.log_metric("f1_score_PNEUMONIA", f1_score_1)
    
print("Training Complete !")

