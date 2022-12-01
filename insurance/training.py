from dkube.sdk import mlflow as dkubemlf

import numpy as np,os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn import preprocessing as skpreprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import mlflow
import pandas as pd
from sklearn import metrics
import joblib

import requests, argparse
requests.packages.urllib3.disable_warnings()

import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--n_estimators', type=int, default=100,
                        help='The number of trees in the forest.')
parser.add_argument('--max_depth', type=int, default=None,
                        help="The maximum depth of the tree.")
parser.add_argument('--max_features', type=int, default=1,
                        help='The number of maximum features provided to each tree in a random forest')
args = parser.parse_args()

n_estimators = args.n_estimators
max_depth = args.max_depth
max_features = args.max_features


# ### MACROS


MLFLOW_EXPERIMENT_NAME = os.getenv('DKUBE_PROJECT_NAME', 'insurance')

# DATASET_URL could be specified as Environment parameters at the time of creating JL or Run

# Define data
INPUT_DATA_URL = os.getenv("DATASET_URL", "https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv")


# Keep track of models.
OUTPUT_MODEL_DIR = os.getcwd()+"/model"


## create OUTPUT_MODEL_DIR
if not os.path.exists(OUTPUT_MODEL_DIR):
    os.makedirs(OUTPUT_MODEL_DIR)


# #### MLFLOW TRACKING INITIALIZATION


import warnings
warnings.filterwarnings('ignore')
exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
if not exp:
    print("Creating experiment...")
    mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT_NAME)




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
#fit random forest regressor to the train set data
rfc = RandomForestRegressor(n_estimators = n_estimators,
                           max_depth=max_depth,
                           max_features=max_features)

# #### ML TRAINING


with mlflow.start_run(run_name="insurance") as run:
    
    model = rfc.fit(x_train, y_train)
    
    y_pred_train = model.predict(x_train)    # Predict on train data.
    y_pred_train[y_pred_train < 0] = y_pred_train.mean()
    y_pred = model.predict(x_test)   # Predict on test data.
    y_pred[y_pred < 0] = y_pred.mean()
    
    #######--- Calculating metrics ---############
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))

    ########--- Logging metrics into Dkube via mlflow ---############
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("RMSE", rmse)

    print(f"mean_absolute_error={mae}")
    
    # Exporting model
    filename = os.path.join(OUTPUT_MODEL_DIR, "model.joblib")
    joblib.dump(model, filename)
    
    # Two ways to save model - log_artifacts() or log_model()
    #mlflow.log_artifacts(OUTPUT_MODEL_DIR, artifact_path="saved_model")
    mlflow.sklearn.log_model(model, "saved_model")
    
    # Record parameters
    mlflow.log_params({"dataset": "https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv",
                       "code": "https://github.com/oneconvergence/dkube-examples/tree/training/insurance",
                       "model": "RandomForestRegressor"})
    
print("Training Complete !")
