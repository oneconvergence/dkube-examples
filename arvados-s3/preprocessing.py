import argparse
import json
import os

import boto3
import numpy as np
import pandas as pd
from dkube.sdk import DkubeApi

if __name__ == "__main__":
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
    MODEL_DIR = "/opt/dkube/output/"
    ########--- Parse for parameters ---########
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default=None, type=str, help="setup URL")
    parser.add_argument(
        "--train_fs", dest="train_fs", required=True, type=str, help="train featureset"
    )
    # parser.add_argument(
    #     "--token", dest="token", required=True, type=str, help="auth token"
    # )
    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()

    # dkubeURL = FLAGS.url
    # Dkube user access token for API authentication
    authToken = os.getenv("DKUBE_USER_ACCESS_TOKEN")
    # Get client handle
    print(f"authToken {authToken}")
    api = DkubeApi(token=authToken)

    out_path = ["/featureset/train"]

    ## Preprocessing training data
    arv_data = np.fromfile("Data0000.dat", dtype=float)
    arv_data = arv_data[~np.isnan(arv_data)]
    arv_data = arv_data.reshape(-1, 1)
    arv_data[arv_data <= 1e308] = 0
    x_feature = [i for i in range(1, 91)]
    arv_data = pd.DataFrame(arv_data, columns=["col1"])
    arv_data["feature"] = x_feature
    ## Commit Featureset
    resp = api.commit_featureset(name=FLAGS.train_fs, df=arv_data)
    arv_data.to_csv("/output-arvados/preprocessed_arvados_data.csv")
