import os
import joblib
import numpy as np
import pandas as pd
from dkube.sdk import DkubeFeatureSet

model_dir = "/model"
test_fs_dir= "/test_fs"

def predict():
    os.system ("ls -l " + test_fs_dir)
    test_df = DkubeFeatureSet.read_features(test_fs_dir)
    print (test_df.columns)
    df = test_df.drop(["PassengerId"], 1)
    df = pd.DataFrame(df).fillna(df.mean())
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    predictions = model.predict(df)
    output = pd.DataFrame({'PassengerId': test_df.PassengerId, 'Survived': predictions})
    output.to_csv("/tmp/prediction.csv", index=False)
    print("predictions generated.")

if __name__ == "__main__":
    predict()
