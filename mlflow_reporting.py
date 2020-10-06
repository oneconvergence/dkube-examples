import os
import warnings
import sys
import mlflow
import logging
import requests
import pandas as pd
import numpy as np
import mlflow.sklearn
from dkube.sdk import *
from urllib.parse import urlparse
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.abspath('../'))

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2



if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url =\
        'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
    try:
        data = pd.read_csv(csv_url, sep=';')
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    ########### Setting Mlflow Tracking uri ###########
    mlflow.set_tracking_uri("http://35.227.115.171:31392")

    ######### Create a dkube training run and extracting the run_id ########
    dkubeURL = 'https://35.227.115.171:32222/'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9jIiwicm9sZSI6Im9wZXJhdG9yIiwiZXhwIjo0ODQxNDQ3MDM1LCJpYXQiOjE2MDE0NDcwMzUsImlzcyI6IkRLdWJlIn0.vIV2-dip23yCUumh3auNNSjXETRa2_NqJgUPyrP1-dIqd3OvDvmWKTIFTser1ycoIpPM4hXDDJxcyiDU3JA5pFkbT0m0Y4V8sT4cQQUpjyIO5mRGvfZYha5vb_-Kw7CLZMpRKmbgxOy7tdZcywlXLqLmItrYjmZWeEvvQPzkKASl9O5d5dsQvx3LZ3bT4Gp1Fps-x0wl0n7G_pY9wQJKIqWvWjoa8tKVVYlnmYBTmne3jguYaGv_dkIDVi7AK2bAJ-_3u9NQnYQS1-oevVfdHu8kfH0fVoxOyOjMWZw2I7gPRHmndR2mhB9EzCsrFUlGzS2SDvoBQ2v0bvHau3vyqA'
    project_name = generate('mlflow-api-reporting')
    project = DkubeProject('oc', name=project_name)
    project.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program', branch='2.0.6')
    training_name= generate('mlflow-api-reporting')
    training = DkubeTraining('oc', name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("sleep 30m")
    api = DkubeApi(URL=dkubeURL, token=authToken)
    api.create_project(project)
    training.add_project(project_name)
    api.create_training_run(training,wait_for_completion=False)
    run_response=api.get_training_run('oc',training_name)
    run_id=run_response["job"]["parameters"]["generated"]["uuid"]

    with mlflow.start_run(run_id):

        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        
      

