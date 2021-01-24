import os
import joblib
import numpy as np
import pandas as pd
from dkube.sdk import DkubeFeatureSet

model_dir = "/model"
test_fs_dir= "/test_fs"

def predict():
    os.system ("ls -l " + test_fs_dir)
    df = DkubeFeatureSet.read_features(test_fs_dir)
    print (df.columns)
    #df = testdf_tmp.drop(["PassengerId","Survived"], 1)
    df = pd.DataFrame(df).fillna(df.mean())
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    predictions = model.predict(df)
    output = pd.DataFrame({'PassengerId': df.PassengerId, 'Survived': predictions})
    output.to_csv("/tmp/prediction.csv", index=False)
    print("predictions generated.")

if __name__ == "__main__":
    predict()
