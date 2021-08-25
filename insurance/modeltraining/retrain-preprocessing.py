import glob
import pandas as pd
import boto3
import os
import json

DATA_DIR = '/data/GT-predict'

config = json.load(open(os.path.join(DATA_DIR, "config.json")))
with open(os.path.join(DATA_DIR, "credentials"), "r") as f:
    creds = f.read()
access_key = creds.split("\n")[1].split("=")[-1].strip()
secret_key = creds.split("\n")[2].split("=")[-1].strip()

session = boto3.session.Session()
s3_client = boto3.resource(
    service_name="s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)


my_bucket = s3_client.Bucket(config["Bucket"])
for s3_object in my_bucket.objects.all():
    path, filename = os.path.split(s3_object.key)
    if filename.endswith('GTpredict_data.csv'):
        my_bucket.download_file(s3_object.key, filename)

final_df = pd.DataFrame()
for file in glob.glob("*/*.csv"):
    data = pd.read_csv(file)
    final_df = pd.concat([final_df,data])

final_df.rename(columns={'GT_target':'charges'}, inplace=True)
final_df.to_csv('/retrain-data/retrain_live_data.csv',index=False)

