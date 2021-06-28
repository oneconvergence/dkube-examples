import argparse
import json
import os
import shutil
import boto3
import numpy as np
import pandas as pd

DATA_DIR = "/opt/dkube/input"
config = json.load(open(os.path.join(DATA_DIR, "config.json")))
with open(os.path.join(DATA_DIR, "credentials"), "r") as f:
    creds = f.read()
access_key = creds.split("\n")[1].split("=")[-1].strip()
secret_key = creds.split("\n")[2].split("=")[-1].strip()

session = boto3.session.Session()
s3_client = boto3.resource(
    service_name="s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=config["Endpoint"],
)

my_bucket = s3_client.Bucket(config["Bucket"])
s3_client.Bucket(config["Bucket"]).download_file(
    "CMU-1/Data0000.dat", "Data0000.dat"
)

shutil.copy("Data0000.dat", "/output-dataset-tc")
