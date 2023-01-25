import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
import tensorflow.keras as k
import pandas as pd
from tensorflow import keras
import numpy as np
from tensorflow.keras import regularizers
import argparse
import cv2
import os
import mlflow

# mlflow metric logging
class loggingCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        mlflow.log_metric("train_loss", logs["loss"], step=epoch)
        mlflow.log_metric("val_loss", logs["val_loss"], step=epoch)
        # output accuracy metric for katib to collect from stdout
        print(f"loss={round(logs['loss'],2)}")


DATA_DIR =  '/opt/dkube/inputs/'
TRAIN_DATA_CLI = DATA_DIR + 'train/clinical/'
TRAIN_DATA_IMG = DATA_DIR + 'train/images/'
TRAIN_DATA_RNA = DATA_DIR + 'train/rna/'

VAL_DATA_CLI = DATA_DIR + 'val/clinical/'
VAL_DATA_IMG = DATA_DIR + 'val/images/'
VAL_DATA_RNA = DATA_DIR + 'val/rna/'

train_df = pd.read_csv(TRAIN_DATA_CLI + "cli_data_processed_train.csv")
val_df = pd.read_csv(VAL_DATA_CLI + "cli_data_processed_val.csv")

Y_train = train_df['days_to_death']
Y_train = np.asarray(Y_train)
Y_train = Y_train.reshape(Y_train.shape[0],1)
train_imgs = list(train_df['bcr_patient_barcode'])

X1_train = train_df.drop(['days_to_death','bcr_patient_barcode'], axis = 1)
X1_train = np.asarray(X1_train)
X1_train = X1_train.reshape(X1_train.shape[0],X1_train.shape[1],1)


Y_val = val_df['days_to_death']
Y_val = np.asarray(Y_val)
Y_val = Y_val.reshape(Y_val.shape[0],1)

X1_val = val_df.drop(['days_to_death','bcr_patient_barcode'], axis = 1)
X1_val = np.asarray(X1_val)
X1_val = X1_val.reshape(X1_val.shape[0],X1_val.shape[1],1)


X2_train = []
X2_val = []
train_imgs = tf.io.gfile.listdir(TRAIN_DATA_IMG)
for each_img in train_imgs:
    ds = cv2.imread(TRAIN_DATA_IMG + each_img, cv2.IMREAD_GRAYSCALE)
    X2_train.append(ds)
X2_train = np.asarray(X2_train)
X2_train = X2_train.reshape(X2_train.shape[0],X2_train.shape[1],X2_train.shape[2],1)

val_imgs = tf.io.gfile.listdir(VAL_DATA_IMG)
for each_img in val_imgs:
    ds = cv2.imread(VAL_DATA_IMG + each_img, cv2.IMREAD_GRAYSCALE)
    X2_val.append(ds)
X2_val = np.asarray(X2_val)
X2_val = X2_val.reshape(X2_val.shape[0],X2_val.shape[1],X2_val.shape[2],1)

def build_cnn_block(img_input_shape, penalty):
    cnn_input = k.layers.Input(shape=img_input_shape, name='img_input')
    cnn_block = k.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', kernel_regularizer=regularizers.l2(penalty),
                activity_regularizer=regularizers.l1(penalty))(cnn_input)
    cnn_block = k.layers.MaxPooling2D(pool_size=(2, 2))(cnn_block)
    cnn_block = k.layers.Dropout(0.25)(cnn_block)
    cnn_block = k.layers.Flatten()(cnn_block)
    cnn_block = k.layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(penalty),
                activity_regularizer=regularizers.l1(penalty))(cnn_block)
    return cnn_block, cnn_input

def build_dense_block(csv_input_shape, penalty):
    csv_input = k.layers.Input(shape=csv_input_shape, name='csv_input')
    dense_block = k.layers.Dense(32,activation='tanh',kernel_regularizer=regularizers.l2(penalty),
                activity_regularizer=regularizers.l1(penalty))(csv_input)
    dense_block = k.layers.Dropout(0.25)(dense_block)
    dense_block = k.layers.Flatten()(dense_block)
    dense_block = k.layers.Dense(32, activation='tanh', kernel_regularizer=regularizers.l2(penalty),
                activity_regularizer=regularizers.l1(penalty))(dense_block)
    return dense_block, csv_input

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", dest = 'epochs', type = int, required=True, help="no. of epochs")
    parser.add_argument("--learningrate", type = float, default=0.01, dest = 'lr', help="learning rate")
    parser.add_argument("--penalty", type = float, default=0.01, dest = 'penalty', help="regularizatio penalty range 0.001 to 0.01")
    parser.add_argument("--modeldir", default='/opt/dkube/output/', dest = 'modeldir', help="path to save model")
    args = parser.parse_args()
    lr = args.lr
    epochs = args.epochs
    penalty = args.penalty
    modeldir = args.modeldir
    step = 50
    img_input_shape = (28,28,1)
    csv_input_shape = (15,1)
    cnn_block, cnn_input = build_cnn_block(img_input_shape, penalty)
    dense_block, csv_input = build_dense_block(csv_input_shape, penalty)
    merged = k.layers.Concatenate()([cnn_block,dense_block])
    merged = k.layers.Dense(16, activation='tanh')(merged)
    merged = k.layers.Dense(8, activation='tanh')(merged)
    merged = k.layers.Dense(1, activation='sigmoid')(merged)
    model = k.models.Model(inputs=[cnn_input, csv_input], outputs=[merged])

    ada_grad = k.optimizers.Adagrad(lr=lr, epsilon=1e-08, decay=0.0)

    model.compile(optimizer=ada_grad, loss='mean_absolute_error')

    model.fit(x=[X2_train, X1_train], y=Y_train, epochs=epochs, verbose=0,
        validation_data=([X2_val, X1_val], Y_val),
        callbacks=[loggingCallback(), tf.keras.callbacks.TensorBoard(log_dir=modeldir)])
    
############### Saving Model  ###############################
    model.save(filepath=os.path.join(modeldir, '1'))
