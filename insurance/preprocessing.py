import os
import json
import glob
import boto3
import argparse
import pandas as pd

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_type", dest="train_type", default='training', type=str, help="training or retraining")

    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    input_train_type = FLAGS.train_type
    
    DATA_DIR = '/data'
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

        if input_train_type == 'retraining' and s3_object.key.startswith('mm-demo/groundtruth'):
            path, filename = os.path.split(s3_object.key)
            if filename.endswith('GTpredict_data.csv'):
                my_bucket.download_file(s3_object.key, filename)

        if input_train_type == 'training' and s3_object.key.startswith('mm-demo/training'):
            path, filename = os.path.split(s3_object.key)
            if filename == 'insurance.csv':
                my_bucket.download_file(s3_object.key,filename)

    if input_train_type == 'training':
        data = pd.read_csv('insurance.csv')
        data.to_csv('/train-data/data.csv',index=False)

    if input_train_type =='retraining':
        final_df = pd.DataFrame()
        for file in glob.glob("*GTpredict_data.csv"):
            data = pd.read_csv(file)
            final_df = pd.concat([final_df,data])

        final_df.rename(columns={'GT_target':'charges'}, inplace=True)
        final_df.to_csv('/train-data/data.csv',index=False)
