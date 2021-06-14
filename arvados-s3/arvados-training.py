import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

DATA_DIR = "/opt/dkube/input"
MODEL_DIR = "/opt/dkube/output/"

arv_data = np.fromfile(DATA_DIR+'/CMU-1/Data0000.dat', dtype=float)
arv_data = arv_data[~np.isnan(arv_data)]
arv_data = arv_data.reshape(-1,1)
arv_data[arv_data <= 1E308] = 0
y_values=[0 if i%2==0 else 1 for i in range(1,91)]

### Training the model ###
arv_clf = RandomForestClassifier(max_depth=2, random_state=0)
arv_clf.fit(arv_data, y_values)

filename = os.path.join(MODEL_DIR, "model.joblib")
joblib.dump(arv_clf, filename)
