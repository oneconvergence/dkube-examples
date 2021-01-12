import os
import numpy as np
import pandas as pd
import argparse

# import sys
import yaml
from dkube.sdk import *

inp_path = ["/dataset/train", "/dataset/test"]
out_path = ["/featureset/train", "/featureset/test"]

if __name__ == "__main__":

    ########--- Parse for parameters ---########

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default=None, type=str, help="setup URL")
    parser.add_argument("--train_fs", dest="train_fs", required=True, type=str, help="train featureset")
    parser.add_argument("--test_fs", dest="test_fs", required=True, type=str, help="test featureset")

    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()

    ########--- Get DKube client handle ---########

    dkubeURL = FLAGS.url
    # Dkube user access token for API authentication
    authToken = os.getenv("DKUBE_USER_ACCESS_TOKEN")
    # Get client handle
    api = DkubeApi(URL=dkubeURL, token=authToken)

    ########--- Extract and load data  ---########

    train_data = pd.read_csv("/dataset/train/train.csv")
    test_data = pd.read_csv("/dataset/test/test.csv")
    print(train_data.describe())

    ########--- Process raw data  ---########

    # Fill in null values with median
    train_data["Age"].fillna(value=train_data["Age"].median(), inplace=True)
    test_data['Age'].fillna(value=test_data['Age'].median(), inplace=True)

    # Drop rows where fare is less than 100
    train_data = train_data[train_data["Fare"] < 100]

    # Fill in null values
    train_data["Embarked"].fillna(method="ffill", inplace=True)
    test_data['Age'].fillna(value=test_data['Age'].median(), inplace=True)
    test_data['Fare'].fillna(test_data['Fare'].median() , inplace = True)

    # Select features for training
    features = ["Pclass", "Sex", "SibSp", "Parch"]
    test_df = pd.get_dummies(test_data[features])
    test_df = pd.concat([test_data[['Age', 'Fare','PassengerId']], test_df], axis=1)
    train_df = pd.get_dummies(train_data[features])
    train_df = pd.concat([train_data[["Age", "Fare", "Survived", "PassengerId"]], train_df], axis=1)
    print(train_df.head())

    ########--- Upload Featureset metadata ---########

    # featureset to use
    fs = [FLAGS.train_fs, FLAGS.test_fs]
    # Features
    k = 0
    for df in [train_df, test_df]:
        # Prepare featurespec - Name, Description, Schema for each feature
        keys = df.keys()
        schema = df.dtypes.to_list()
        featureset_metadata = []
        print(fs[k], out_path[k])
        for i in range(len(keys)):
            metadata = {}
            metadata["name"] = str(keys[i])
            metadata["description"] = None
            metadata["schema"] = str(schema[i])
            featureset_metadata.append(metadata)
        
        # Convert featureset metadata (featurespec) to yaml
        featureset_metadata = yaml.dump(featureset_metadata, default_flow_style=False)
        with open("fspec.yaml", "w") as f:
            f.write(featureset_metadata)
        # Upload featureset metadata (featurespec)
        resp = api.upload_featurespec(featureset=fs[k], filepath="fspec.yaml")
        print("featurespec upload response:", resp)
        
        ########--- Commit features ---########
        # Featureset
        featureset = DkubeFeatureSet()
        # Specify features path - mounted as output
        featureset.update_features_path(path=out_path[k])
        # Write features - Dataframe
        featureset.write(df)
        k =+1
    # Commit featuresset
    resp = api.commit_features()
    print("featureset commit response:", resp)