import os
import joblib
import pandas as pd
from joblib import dump, load
from sklearn import preprocessing as skpreprocessing
from sklearn.linear_model import SGDRegressor 


out_path = '/mm/retrained-model'

live_data = pd.read_csv('/retrain-data/retrain_live_data.csv')

for col in ['sex', 'smoker', 'region']:
        if (live_data[col].dtype == 'object'):
            le = skpreprocessing.LabelEncoder()
            le = le.fit(live_data[col])
            live_data[col] = le.transform(live_data[col])

x_live = live_data.drop(['charges','timestamp','unique_id'],axis = 1)
y_live = live_data['charges']

train_model = load('/model/model.joblib')


train_model.partial_fit(x_live,y_live)

filename = os.path.join(out_path, "model.joblib")
joblib.dump(train_model, filename)

