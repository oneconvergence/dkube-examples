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

inp_data_path = '/train-data'
out_model_path = "/model"

if __name__ == "__main__":
    
    data = pd.read_csv(inp_data_path+'/data.csv')
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
    sgd = SGDRegressor()
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
    filename = os.path.join(out_model_path, "model.joblib")
    joblib.dump(sgd_model, filename)
