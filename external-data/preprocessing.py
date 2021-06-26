import boto3
import json
import os
import joblib
import pandas as pd
import argparse
from dkube.sdk import DkubeApi

if __name__ == "__main__":
    
    DATA_DIR = '/opt/dkube/input'

    config = json.load(open(os.path.join(DATA_DIR,'config.json')))

    with open(os.path.join(DATA_DIR,'credentials'), 'r') as f:
        creds = f.read()
       
    access_key = creds.split('\n')[1].split('=')[-1].strip()
    secret_key = creds.split('\n')[2].split('=')[-1].strip()

    session = boto3.session.Session()
    s3_client = boto3.resource(service_name='s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)

    s3_client.Bucket(config['Bucket']).download_file('datasets/heart-data/heart.csv', 'heart.csv')

    ########--- Parse for parameters ---########
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default=None, type=str, help="setup URL")
    parser.add_argument("--train_fs", dest="train_fs", required=True, type=str, help="train featureset")
    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    
    dkubeURL = FLAGS.url
    # Dkube user access token for API authentication
    authToken = os.getenv("DKUBE_USER_ACCESS_TOKEN")
    # Get client handle
    api = DkubeApi(URL=dkubeURL, token=authToken)

    out_path = ["/featureset/train"]

    ## Preprocessed training data
    train_data=pd.read_csv('heart.csv')
    train_data = train_data.drop('ca',axis = 1)
    ## Commit Featureset
    resp = api.commit_featureset(name=FLAGS.train_fs, df=train_data)
