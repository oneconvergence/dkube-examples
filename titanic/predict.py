import os
import joblib
import numpy as np
import pandas as pd

model_dir = "/model"

def predict():
    test_df = pd.read_csv(os.path.join(model_dir, "test.csv"))
    testdf_tmp = test_df
    df = testdf_tmp.drop("PassengerId", 1)
    #df = testdf_tmp.drop(["PassengerId","Survived"], 1)
    df = pd.DataFrame(df).fillna(df.mean())
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    predictions = model.predict(df)
    output = pd.DataFrame({'PassengerId': test_df.PassengerId, 'Survived': predictions})
    output.to_csv("/tmp/prediction.csv", index=False)
    print("predictions generated.")

if __name__ == "__main__":
    predict()
