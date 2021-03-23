import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import requests, os
import argparse
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import mlflow
from sklearn import metrics
from dkube.sdk import *
import joblib

inp_path = "/opt/dkube/in"
out_path = "/opt/dkube/out"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default=None, type=str, help="setup URL")
    parser.add_argument("--fs", dest="fs", required=True, type=str, help="featureset")

    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    dkubeURL = FLAGS.url
    fs = FLAGS.fs

    ########--- Read features from input FeatureSet ---########

    # Featureset API
    authToken = os.getenv("DKUBE_USER_ACCESS_TOKEN")
    # Get client handle
    api = DkubeApi(URL=dkubeURL, token=authToken)

    # Read features
    feature_df = api.read_featureset(name = fs)  # output: data

    ########--- Train ---########
    insurance_input = feature_df.drop(['charges'],axis=1)
    insurance_target = feature_df['charges']
    
    #stadardize data
    x_scaled = StandardScaler().fit_transform(insurance_input)
    x_train, x_test, y_train, y_test = train_test_split(x_scaled,
                                                    insurance_target,
                                                    test_size = 0.25,
                                                    random_state=1211)
    #fit linear model to the train set data
    linReg = LinearRegression()
    linReg_model = linReg.fit(x_train, y_train)
    
    y_pred_train = linReg.predict(x_train)    # Predict on train data.
    y_pred_train[y_pred_train < 0] = y_pred_train.mean()
    y_pred = linReg.predict(x_test)   # Predict on test data.
    y_pred[y_pred < 0] = y_pred.mean()
    
    #######--- Calculating metrics ---############
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    intersept = linReg.intercept_
    print('Mean Absolute Error:', mae)  
    print('Mean Squared Error:', mse)  
    print('Root Mean Squared Error:', rmse)
    print('Intercept: ', intersept)

    ########--- Logging metrics into Dkube via mlflow ---############
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("intercept", intersept)

    # Exporting model
    filename = os.path.join(out_path, "model.joblib")
    joblib.dump(linReg_model, filename)
