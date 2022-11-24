#!/usr/bin/env python
# coding: utf-8

# In[111]:


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
from sklearn.linear_model import LinearRegression
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

# In[112]:


MLFLOW_EXPERIMENT_NAME = os.getenv('DKUBE_PROJECT_NAME', 'insurance')

# Experiment with this parameter. 
NUM_EPOCHS = os.getenv("EPOCHS", 10)

# Define data
INPUT_DATA_URL = os.getenv("DATASET_URL", "https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv")


# Keep track of models.
OUTPUT_MODEL_DIR = os.getcwd()+"/model"
## optional. If you haven't created a model repo, set DKUBE_MODEL_REPO to None
DKUBE_MODEL_REPO = os.getenv('MODEL_REPO', None)

## create OUTPUT_MODEL_DIR
if not os.path.exists(OUTPUT_MODEL_DIR):
    os.makedirs(OUTPUT_MODEL_DIR)


# #### MLFLOW TRACKING INITIALIZATION

# In[113]:


import warnings
warnings.filterwarnings('ignore')
exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
if not exp:
    print("Creating experiment...")
    mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT_NAME)
mlflow.tensorflow.autolog(silent=True)


# In[114]:



data = pd.read_csv(INPUT_DATA_URL)
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
#fit linear model to the train set data
lm = SGDRegressor(loss='squared_error', max_iter=NUM_EPOCHS, n_iter_no_change=10, early_stopping=True)

# other linear models user could try
#lm = SGDRegressor(loss='squared_epsilon_insensitive', max_iter=NUM_EPOCHS, n_iter_no_change=10, early_stopping=True)
#lm = LinearRegression()


# #### ML TRAINING

# In[115]:


#runid = dkubemlf.create_run(code=DKUBE_INPUT_CODE, dataset=DKUBE_INPUT_DATASET,output=DKUBE_OUTPUT_MODEL)
runid = dkubemlf.create_run(output=DKUBE_OUTPUT_MODEL)


# In[116]:


with mlflow.start_run(run_name="insurance", run_id=runid) as run:
    
    model = lm.fit(x_train, y_train)
    
    y_pred_train = model.predict(x_train)    # Predict on train data.
    y_pred_train[y_pred_train < 0] = y_pred_train.mean()
    y_pred = model.predict(x_test)   # Predict on test data.
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
    mlflow.log_metric("RMSE", rmse)
    
    # Exporting model
    filename = os.path.join(OUTPUT_MODEL_DIR, "model.joblib")
    joblib.dump(model, filename)
    
    # Two ways to save model - log_artifacts() or log_model()
    #mlflow.log_artifacts(OUTPUT_MODEL_DIR, artifact_path="saved_model")
    mlflow.sklearn.log_model(model, "saved_model")
    
    # Record parameters?
    mlflow.log_params({"dataset": "https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv",
                       "code": "https://github.com/oneconvergence/dkube-examples/tree/training/insurance",
                       "linear model": "SGDRegressor",
                       "max_iterations": NUM_EPOCHS})
    
print("Training Complete !")


# In[ ]:




