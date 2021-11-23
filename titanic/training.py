import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tensorflow import keras
from keras import backend as K
from sklearn.model_selection import train_test_split
import tensorflow as tf
import transform_data
from sklearn import preprocessing
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from mlflow import log_metric
import argparse, os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', type=int, default=1, help='Batch size for training.')
parser.add_argument('--num_epochs', type=int, default=int(os.getenv("EPOCHS","5")), help='Number of epochs to train for.')
parser.add_argument('--data_source',type=str,default='local',help='Data source')
args = parser.parse_args()

batch_size = args.batch_size
epochs = args.num_epochs
data_source = args.data_source
print ("Number of epochs:", epochs)

train_path = "/train-data"
MODEL_DIR = "/model/"

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


## loading dataset
train = pd.read_csv(train_path+'/data.csv')
if data_source == 'local' or data_source == 'aws_s3':
    train = train[train["Fare"] < 100]
    transformer = transform_data.Transformer()
    train = transformer.preprocess(train)
y_train = train["Survived"].values
x_train = train.drop(['Survived','PassengerId','timestamp'],axis=1).values
X_train, X_test, Y_train, Y_test = train_test_split(x_train, y_train, test_size=0.3, random_state=512)

# Network
model = Sequential()
model.add(Dense(12, activation='relu', input_shape=(7,)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc',f1_m,precision_m, recall_m])

model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, verbose=0, validation_split=0.1)

# evaluate the model
loss, accuracy, f1_score, precision, recall = model.evaluate(X_test, Y_test, verbose=0)

## logging the metrics
log_metric("accuracy",accuracy)
log_metric("f1_score",f1_score)
log_metric("precision",precision)
log_metric("recall",recall)

model.save(MODEL_DIR + 'weights.h5')
tf.keras.backend.set_learning_phase(0)  # Ignore dropout at inference
tf.saved_model.save(model,MODEL_DIR + str(1))
