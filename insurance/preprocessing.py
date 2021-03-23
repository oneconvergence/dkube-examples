import numpy as np
import pandas as pd
import os
import argparse
import yaml
from sklearn import preprocessing as skpreprocessing

from dkube.sdk import *

inp_dir = "/opt/dkube/in"
out_path = "/opt/dkube/out"

if __name__ == "__main__":

    ########--- Parse for parameters ---########

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", default=None, type=str, help="setup URL")
    parser.add_argument("--fs", dest="fs", required=True, type=str, help="featureset")

    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    fs = FLAGS.fs

    ########--- Get DKube client handle ---########

    dkubeURL = FLAGS.url
    # Dkube user access token for API authentication
    authToken = os.getenv("DKUBE_USER_ACCESS_TOKEN")
    # Get client handle
    api = DkubeApi(URL=dkubeURL, token=authToken)

    ########--- Extract and load data  ---######
    
    insurance = pd.read_csv(os.path.join(inp_dir, "insurance.csv"))

    ########--- Feature Engineering ---#######
    
    for col in ['sex', 'smoker', 'region']:
        if (insurance[col].dtype == 'object'):
            le = skpreprocessing.LabelEncoder()
            le = le.fit(insurance[col])
            insurance[col] = le.transform(insurance[col])
            print('Completed Label encoding on',col)

    # Commit featureset
    resp = api.commit_featureset(name=fs, df=insurance)
    print("featureset commit response:", resp)
