import os
import pandas as pd

from dkube.sdk import *

import warnings
warnings.filterwarnings("ignore")
import requests, argparse
requests.packages.urllib3.disable_warnings()

MLFLOW_EXPERIMENT_NAME = os.getenv('DKUBE_PROJECT_NAME')

## Get the username & token and create the DKube SDK API ariable

SERVING_DKUBE_URL = os.getenv("DKUBE_URL")
SERVING_DKUBE_TOKEN = os.getenv("DKUBE_USER_ACCESS_TOKEN")
SERVING_DKUBE_USERNAME = os.getenv("DKUBE_USER_LOGIN_NAME")

dapi = DkubeApi(URL=SERVING_DKUBE_URL,token=SERVING_DKUBE_TOKEN)
pre_api = DkubePreprocessing(SERVING_DKUBE_USERNAME)
dataset_info = DkubeDataset("larryc1200", name="ins-lc-dataset")

#DATASET_URL could be specified as Environment parameters at the time of creating JL or Run

# Define data
INPUT_DATA_URL = os.getenv("DATASET_URL", "https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv")

## Get the original data
data = pd.read_csv(INPUT_DATA_URL)

## Choose which columns to keep
insurance_filtered = data.drop(['age'], axis=1)

## Set up the API parameters for creating an updated dataset
DATASET_REPO_NAME = "ins-lc-dataset"
DATASET_MOUNT_PATH = "/dataset/"

## Create the new dataset with the filtered data
# dapi.create_dataset(dataset_info)

print(DATASET_REPO_NAME)
print(DATASET_MOUNT_PATH)
pre_api.add_output_dataset(name=DATASET_REPO_NAME, mountpath=DATASET_MOUNT_PATH)
insurance_filtered.to_csv(DATASET_MOUNT_PATH + "test.csv")