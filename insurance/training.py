#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time
import random
import string
from dkube.sdk import mlflow as dkubemlf

import numpy as np,os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn import preprocessing as skpreprocessing
from sklearn.linear_model import SGDRegressor   
from sklearn.preprocessing import StandardScaler
import mlflow
import pandas as pd
from sklearn import metrics
import joblib

import requests
requests.packages.urllib3.disable_warnings()

import warnings
warnings.filterwarnings("ignore")


# ### MACROS

# In[7]:


# Define where the input data dir and model output dir are
INPUT_DATA_DIR = "/mnt/data"
OUTPUT_MODEL_DIR = "/mnt/model"
NUM_EPOCHS = os.getenv("EPOCHS", 2000)
MLFLOW_EXPERIMENT_NAME = os.getenv('DKUBE_PROJECT_NAME', 'insurance')
DKUBE_INPUT_CODE = "insurance"
DKUBE_INPUT_DATASET = "insurance"
DKUBE_OUTPUT_MODEL = "insurance"
MLFLOW_EXPERIMENT_NAME


# #### MLFLOW TRACKING INITIALIZATION

# In[8]:


import warnings
warnings.filterwarnings('ignore')
exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
if not exp:
    print("Creating experiment...")
    mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT_NAME)
mlflow.tensorflow.autolog(silent=True)


# In[9]:



data = pd.read_csv(INPUT_DATA_DIR+'/insurance.csv')
insurance_input = data.drop(['charges','timestamp','unique_id'],axis=1)
insurance_target = data['charges']
    
for col in ['sex', 'smoker', 'region']:
    if (insurance_input[col].dtype == 'object'):
        le = skpreprocessing.LabelEncoder()
        le = le.fit(insurance_input[col])
        insurance_input[col] = le.transform(insurance_input[col])
        print('Completed Label encoding on',col)
    
#standardize data
x_scaled = StandardScaler().fit_transform(insurance_input)
x_train, x_test, y_train, y_test = train_test_split(x_scaled,
                                                    insurance_target,
                                                    test_size = 0.25,
                                                    random_state=1211)
#fit sgd model to the train set data
sgd = SGDRegressor(loss='squared_epsilon_insensitive', max_iter=NUM_EPOCHS, n_iter_no_change=10, early_stopping=True)


# #### ML TRAINING

# In[10]:


runid = dkubemlf.create_run(code=DKUBE_INPUT_CODE, dataset=DKUBE_INPUT_DATASET,output=DKUBE_OUTPUT_MODEL)


# In[11]:


with mlflow.start_run(run_id=runid) as run:
    
    sgd_model = sgd.fit(x_train, y_train)
    
    y_pred_train = sgd_model.predict(x_train)    # Predict on train data.
    y_pred_train[y_pred_train < 0] = y_pred_train.mean()
    y_pred = sgd_model.predict(x_test)   # Predict on test data.
    y_pred[y_pred < 0] = y_pred.mean()
    
    #######--- Calculating metrics ---############
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    
    print('Mean Absolute Error:', mae)  
    print('Mean Squared Error:', mse)  
    print('Root Mean Squared Error:', rmse)

    ########--- Logging metrics into Dkube via mlflow ---############
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)

    # Exporting model
    filename = os.path.join(OUTPUT_MODEL_DIR, "model.joblib")
    joblib.dump(sgd_model, filename)
    
    mlflow.log_artifacts(OUTPUT_MODEL_DIR, artifact_path="saved_model")
    
print("Training Complete !")


# In[ ]:




