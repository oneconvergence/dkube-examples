import json
import os

import boto3
import joblib
import numpy as np
import pandas as pd
from dkube.sdk import DkubeFeatureSet
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = "/model/"
train_path = "/featureset/train"

train = DkubeFeatureSet.read_features(train_path)
arv_data = pd.DataFrame(train)
x_train = arv_data.iloc[:, :-1].values
y_values = [0 if i % 2 == 0 else 1 for i in range(1, 91)]
### Training the model ###
arv_clf = RandomForestClassifier(max_depth=2, random_state=0)
arv_clf.fit(x_train, y_values)

filename = os.path.join(MODEL_DIR, "model.joblib")
joblib.dump(arv_clf, filename)
