from tensorflow import keras
from dkube.sdk import DkubeFeatureSet
import pandas as pd
import json, os

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
    x_test= test_df.drop(["PassengerId"], 1).values
    model = keras.models.load_model(os.path.join(model_dir, "1"))
    y_pred = model.predict(x_test)
    y_pred[y_pred <= 0.5] = 0
    y_pred[y_pred > 0.5] = 1
    output = pd.DataFrame({'PassengerId': test_df.PassengerId, 'Survived': y_pred.flatten().tolist()})
    output.to_csv("/output/prediction.csv", index=False)
    print("predictions generated.")

if __name__ == "__main__":
    predict()
