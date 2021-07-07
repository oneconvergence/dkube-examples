import pandas as pd
import joblib
from dkube.sdk import DkubeFeatureSet
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = "/model/"
train_path = "/featureset/train"

train = DkubeFeatureSet.read_features(train_path)
train_data = pd.DataFrame(train)
x_train=train_data.iloc[:,:-1].values
y_train=train_data.iloc[:,12].values
rf = RandomForestClassifier(n_estimators = 1000, random_state = 1)
rf.fit(x_train, y_train)
######## Model Saving ########
filename = MODEL_DIR + '/model.joblib'
joblib.dump(rf, filename)
