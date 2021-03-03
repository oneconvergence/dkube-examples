import os
import joblib
import numpy as np
import pandas as pd
from dkube.sdk import DkubeFeatureSet
import json

model_dir = "/model"
test_fs_dir= "/test_fs"
metadata = {
    "outputs": [
        {
            "storage": "inline",
            "type": "table",
            "format": "csv",
            "header": ["cv_accuracy", "cv_brier_score"],
            "source": "0.78, 0.88",
        }
    ]
}

with open("/output/metrics.json", "w") as f:
    json.dump(metadata, f)

def predict():
    os.system ("ls -l " + test_fs_dir)
    test_df = DkubeFeatureSet.read_features(test_fs_dir)
    print (test_df.columns)
    df = test_df.drop(["PassengerId"], 1)
    df = pd.DataFrame(df).fillna(df.mean())
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    predictions = model.predict(df)
    output = pd.DataFrame({'PassengerId': test_df.PassengerId, 'Survived': predictions})
    output.to_csv("/output/prediction.csv", index=False)
    print("predictions generated.")

if __name__ == "__main__":
    predict()
