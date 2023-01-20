import os
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as skpreprocessing
from sklearn.preprocessing import StandardScaler
import mlflow
from mlflow.models.signature import infer_signature
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import warnings
warnings.filterwarnings("ignore")
import requests, argparse
requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, default=10,
                        help='The number of epochs for training')
parser.add_argument('--learning_rate', type=float, default=0.01,
                        help="learning rate for optimizer")
args = parser.parse_args()

NUM_EPOCHS = int(os.getenv("EPOCHS", args.epochs))

LEARNING_RATE = args.learning_rate

inp_data_path = '/train-data'
out_model_path = "/model"

# mlflow metric logging
class loggingCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        mlflow.log_metric("train_loss", logs["loss"], step=epoch)
        mlflow.log_metric("val_loss", logs["val_loss"], step=epoch)
        # output accuracy metric for katib to collect from stdout
        print(f"loss={round(logs['loss'],2)}")

if __name__ == "__main__":
    
    data = pd.read_csv(inp_data_path+'/data.csv')
    insurance_input = data.drop(['charges','timestamp','unique_id'],axis=1)
    insurance_target = data['charges']
    
    for col in ['sex', 'smoker', 'region']:
        if (insurance_input[col].dtype == 'object'):
            le = skpreprocessing.LabelEncoder()
            le = le.fit(insurance_input[col])
            insurance_input[col] = le.transform(insurance_input[col])
            print('Completed Label encoding on',col)
    
    #standardize data
    x_scaled = StandardScaler().fit_transform(insurance_input)
    x_train, x_test, y_train, y_test = train_test_split(x_scaled,
                                                        insurance_target.values,
                                                        test_size = 0.25,
                                                        random_state=1211)
    #fit random forest regressor to the train set data
    tf.random.set_seed(42)  #first we set random seed
    model = keras.Sequential([
        layers.InputLayer(input_shape=(6)),
        layers.Dense(64, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(lr=LEARNING_RATE))


    with mlflow.start_run(run_name="insurance") as run:
        model.fit(x_train, y_train, epochs = NUM_EPOCHS, verbose=0,
                    validation_split=0.1, callbacks=[loggingCallback()])
        
        # Exporting model
        model.save(filepath=os.path.join(out_model_path, '1'))
        
        # Two ways to save model - log_artifacts() or log_model()
        mlflow.log_artifacts(out_model_path) ## For tf-serving
        signature = infer_signature(x_test, model.predict(x_test))
        mlflow.keras.log_model(keras_model=model, artifact_path=None, signature=signature)
            
        # Record parameters
        mlflow.log_params({"dataset": "https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv",
                        "code": "https://github.com/oneconvergence/dkube-examples/tree/monitoring/",
                        "model": "Deep Neural Network"})
    print("Training Complete !")
