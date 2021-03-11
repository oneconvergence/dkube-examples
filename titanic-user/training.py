import joblib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import argparse
import numpy as np
import pandas as pd
import requests, os
import pyarrow as pa
import pyarrow.parquet as pq
from tensorflow import keras

import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from dkube.sdk import DkubeFeatureSet
from mlflow import log_metric
from sklearn.model_selection import train_test_split
from dkube.sdk import *

inp_path = "/titanic-train"
MODEL_DIR= "/model/"
test_path = "/titanic-test"


if __name__ == "__main__":

    ########--- Parse for parameters ---########

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default=None, type=str, help="setup URL")
    parser.add_argument("--train_fs", dest="train_fs", required=True, type=str, help="featureset")
    parser.add_argument('--batch_size', type=int, default=1, help='Batch size for training.')
    parser.add_argument('--num_epochs', type=int, default=int(os.getenv("EPOCHS","20")), help='Number of epochs to train for.')
    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    dkubeURL = FLAGS.url
    train_fs = FLAGS.train_fs
    batch_size = FLAGS.batch_size
    epochs = FLAGS.num_epochs
    print ("Number of epochs:", epochs)

    ########--- Read features from input FeatureSet ---########

    # Featureset API
    authToken = os.getenv("DKUBE_USER_ACCESS_TOKEN")
    # Get client handle
    api = DkubeApi(URL=dkubeURL, token=authToken)

    # Read features
    feature_df = api.read_featureset(name = train_fs)  # output: data

    train, val = train_test_split(feature_df, test_size=0.2)
    ########--- Train ---########

    # preparing input output pairs
    y_train = train["Survived"].values
    x_train = train.drop(["PassengerId","Survived"], 1).values

    # Network
    model = Sequential()
    model.add(Dense(12, activation='relu', input_shape=(7,)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

    # mlflow metric logging
    class loggingCallback(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            accuracy_metric = "accuracy"
            if "acc" in logs:
                accuracy_metric = "acc"

            log_metric ("train_loss", logs["loss"], step=epoch)
            log_metric ("train_accuracy", logs[accuracy_metric], step=epoch)
            log_metric ("val_loss", logs["val_loss"], step=epoch)
            log_metric ("val_accuracy", logs["val_" + accuracy_metric], step=epoch)
            # output accuracy metric for katib to collect from stdout
            print(f"accuracy={round(logs['val_' + accuracy_metric],2)}")

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0, validation_split=0.1, 
            callbacks=[loggingCallback(), tf.keras.callbacks.TensorBoard(log_dir=MODEL_DIR)])

    model.save(MODEL_DIR + 'weights.h5')
    tf.keras.backend.set_learning_phase(0)  # Ignore dropout at inference
    tf.saved_model.save(model,MODEL_DIR + str(1))
              
