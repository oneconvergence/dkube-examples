import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import requests, os
import argparse
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import mlflow
from dkube.sdk import *

inp_path = "/titanic-train"
out_path = "/model"
test_path = "/titanic-test"


if __name__ == "__main__":

    ########--- Read features from input FeatureSet ---########

    # Featureset API
    featureset = DkubeFeatureSet()
    # Specify featureset path
    featureset.update_features_path(path=inp_path)

    # Read features
    data = featureset.read()  # output: response json with data
    feature_df = data["data"]
    train, val = train_test_split(feature_df, test_size=0.2)
    ########--- Train ---########

    # preparing input output pairs
    y = train["Survived"].values
    x = train.drop(["PassengerId","Survived"], 1).values

    # Training random forest classifier
    model_RFC = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model_RFC.fit(x, y)
    predictions = model_RFC.predict(x)

    ########--- Log metrics to DKube ---########

    # Calculating accuracy
    accuracy = accuracy_score(y, predictions)
    # logging acuracy to DKube
    mlflow.log_metric("accuracy", accuracy)

    ########--- Write model to DKube ---########

    # Exporting model
    filename = os.path.join(out_path, "model.joblib")
    joblib.dump(model_RFC, filename)

    # Writing test data
    featureset = DkubeFeatureSet()
    # Specify featureset path
    featureset.update_features_path(path=test_path)
    # Read features
    data = featureset.read()  # output: response json with data
    test_df = data["data"]
    test_df.to_csv(os.path.join(out_path, "test.csv"), index=False)
    val.to_csv(os.path.join(out_path, "val.csv"), index=False)