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
from dkube.sdk import DkubeFeatureSet

train_path = "/featureset/train"
test_path = "/featureset/test"
out_path = "/model"

if __name__ == "__main__":

    # Read features
    train = DkubeFeatureSet.read_features(train_path)
    val = DkubeFeatureSet.read_features(test_path)

    print(train.head())
    print(val.head())
    
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