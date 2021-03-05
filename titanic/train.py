import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from dkube.sdk import DkubeFeatureSet
from mlflow import log_metric
import argparse, os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', type=int, default=1, help='Batch size for training.')
parser.add_argument('--num_epochs', type=int, default=int(os.getenv("EPOCHS","20")), help='Number of epochs to train for.')
args = parser.parse_args()

batch_size = args.batch_size
epochs = args.num_epochs
print ("Number of epochs:", epochs)

train_path = "/featureset/train"
MODEL_DIR = "/model/"

#load featureset
train = DkubeFeatureSet.read_features(train_path)
train = pd.DataFrame(train).fillna(train.mean())
y_train = train["Survived"].values
x_train= train.drop(["PassengerId","Survived"], 1).values

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