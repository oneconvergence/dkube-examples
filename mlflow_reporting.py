import argparse
import logging
import os
import sys
import warnings
from urllib.parse import urlparse

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import requests
from dkube.sdk import *
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def create_dkube_run(url, token, user):
    GIT_PROJECT_URL = 'https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program'
    # Create DKube resources
    api = DkubeApi(URL=url, token=token)

    try:
        api.get_code(user, "mlflow-test")
    except Exception as exc:
        logger.info("Creating code (mlflow-test) for user " + user)
        code = DkubeCode(user, name="mlflow-test")
        code.update_git_details(GIT_PROJECT_URL, branch='2.0.6')
        api.create_code(code)
    else:
        logger.info("code (mlflow-test) already exist, skipping creation..")

    training_name = generate('mlflow-test')
    logger.info("Creating a training run (" +
                training_name + ") for user " + user)

    training = DkubeTraining(user, name=training_name,
                             description='Run to test mlflow metric reporting')
    training.update_container(
        framework="tensorflow_1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("sleep 30m")
    training.add_code('mlflow-test')
    api.create_training_run(training, wait_for_completion=False)

    run_response = api.get_training_run(user, training_name)
    run_id = run_response["job"]["parameters"]["generated"]["uuid"]

    logger.info("DKube run id (" + run_id +
                "), metrics can be reported against it")

    return run_id


def mlflow_train_and_report(url, token, runid):
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

    alpha = 0.5
    l1_ratio = 0.5

    # Following envs must be set for mlflow reporting to work
    os.environ['MLFLOW_TRACKING_TOKEN'] = str(token)
    os.environ['MLFLOW_TRACKING_INSECURE_TLS'] = "true"
    os.environ['MLFLOW_RUN_ID'] = str(runid)
    os.environ["MLFLOW_TRACKING_URI"] = str(url)

    logger.info("Setting MLFlow tracking URL to " + url)

    with mlflow.start_run(runid):

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


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    parser = argparse.ArgumentParser(description='Argument parser')
    # Add the arguments
    parser.add_argument('url',
                        metavar='url',
                        type=str,
                        help='URL to DKube platform.')
    parser.add_argument('token',
                        metavar='token',
                        type=str,
                        help='DKube access token.')

    parser.add_argument('user',
                        metavar='user',
                        type=str,
                        help='DKube user.')

    flags = parser.parse_args()

    url   = flags.url
    token = flags.token
    user  = flags.user

    runid = create_dkube_run(url, token, user)

    mlflow_train_and_report(url, token, runid)
