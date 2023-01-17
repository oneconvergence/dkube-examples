import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
import tensorflow.keras as k
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard, LambdaCallback
from tensorflow.keras import optimizers
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model.signature_def_utils import predict_signature_def
from tensorflow.python.saved_model import tag_constants
import pandas as pd
import pydicom
import numpy as np
from tensorflow.keras import regularizers
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_log_error,mean_squared_error
from tensorflow.keras.callbacks import TensorBoard
import argparse
import requests
import cv2, json
import os

def log_metrics(key, value, epoch, step):
    url = "http://dkube-exporter.dkube:9401/mlflow-exporter"
    train_metrics = {}
    train_metrics['mode']="train"
    train_metrics['key'] = key
    train_metrics['value'] = value
    train_metrics['epoch'] = epoch
    train_metrics['step'] = step
    train_metrics['jobid']=os.getenv('DKUBE_JOB_ID')
    train_metrics['run_id']=os.getenv('DKUBE_JOB_UUID')
    train_metrics['username']=os.getenv('DKUBE_USER_LOGIN_NAME')
    requests.post(url, json = train_metrics)

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

'''def write_log(callback, names, logs, batch_no):
    for name, value in zip(names, logs):
        summary = tf.Summary()
        summary_value = summary.value.add()
        summary_value.simple_value = value
        summary_value.tag = name
        callback.writer.add_summary(summary, batch_no)
        callback.writer.flush()'''

def write_log(writer, names, logs, batch_no):
    for name, value in zip(names, logs):
        with writer.as_default():
            tf.summary.scalar(name, value, batch_no)
            writer.flush()


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
    export_path = modeldir
    log_path = modeldir + '/logs'
    cnn_block, cnn_input = build_cnn_block(img_input_shape, penalty)
    dense_block, csv_input = build_dense_block(csv_input_shape, penalty)
    merged = k.layers.Concatenate()([cnn_block,dense_block])
    merged = k.layers.Dense(16, activation='tanh')(merged)
    merged = k.layers.Dense(8, activation='tanh')(merged)
    merged = k.layers.Dense(1, activation='sigmoid')(merged)
    model = k.models.Model(inputs=[cnn_input, csv_input], outputs=[merged])

    ada_grad = k.optimizers.Adagrad(lr=lr, epsilon=1e-08, decay=0.0)
    model.compile(optimizer=ada_grad, loss='mse',metrics=['mae'])
    train_names = ['train_loss', 'train_mae', 'train_r2']
    val_names = ['val_loss', 'val_mae', 'val_r2']
    
    writer = tf.summary.create_file_writer(log_path)
    no_of_pass = int(len(X2_train)/step)
    pass_count = 1
    for each_epoch in range(epochs):
        idx = 0
        train_metrics = []
        val_metrics = []
        for each_pass in range(1 , no_of_pass+1):
            x1 = X1_train[idx:each_pass*step]
            x2 = X2_train[idx:each_pass*step]
            y = Y_train[idx:each_pass*step]
            logs = model.train_on_batch(x=[x2, x1], y= y)
            train_preds = model.predict([x2, x1])
            logs.append(r2_score(y, train_preds))
            write_log(writer, train_names, logs, each_epoch)

            val_logs = model.test_on_batch(x=[X2_val,X1_val], y= Y_val)
            val_preds = model.predict([X2_val,X1_val])
            val_logs.append(r2_score(Y_val, val_preds))
            write_log(writer, train_names, val_logs, each_epoch)
            idx = each_pass*step
            train_metrics.append(logs)
            val_metrics.append(val_logs)
            bt_step = step * pass_count
            print('Epoch = ', each_epoch+1, ', step = ', bt_step, ', loss = ',logs[0], ', val_loss = ', val_logs[0])
            pass_count += 1
            
        train_metrics = np.asarray(train_metrics)
        train_metrics = np.average(train_metrics, axis=0)
        log_metrics('mse', train_metrics[0], each_epoch + 1, bt_step)
        log_metrics('mae', train_metrics[1], each_epoch + 1, bt_step)
        log_metrics('r2', train_metrics[2], each_epoch + 1, bt_step)
        
############### Saving Model  ###############################
    version = 0
    if not tf.io.gfile.exists(export_path):
        tf.io.gfile.makedirs(export_path)
    model_contents = tf.io.gfile.listdir(export_path)

    saved_models = []
    for mdir in model_contents:
        if mdir != 'logs' and mdir != 'metrics':
            saved_models.append(int(mdir))
    print(saved_models)
    if len(saved_models) < 1:
        version = 1
    else:
        version = max(saved_models) + 1
    model.save(export_path + str(version))
