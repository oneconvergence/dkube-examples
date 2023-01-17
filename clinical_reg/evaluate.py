import tensorflow as tf
import numpy as np
import requests
import tensorflow as tf
import cv2, argparse
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_log_error,mean_squared_error

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modeldir", default='/opt/dkube/inputs/model/', dest = 'modeldir', help="path to save model")
    args = parser.parse_args()

    modeldir = args.modeldir
    export_path = modeldir + '/weights.h5'

    DATA_DIR = '/opt/dkube/inputs/'
    TEST_DATA_CLI = DATA_DIR + 'test/clinical/'
    TEST_DATA_IMG = DATA_DIR + 'test/images/'
    TEST_DATA_RNA = DATA_DIR + 'test/rna/'

    test_df = pd.read_csv(TEST_DATA_CLI + "cli_data_processed_test.csv")
    Y = test_df['days_to_death']
    Y = np.asarray(Y)
    Y = Y.reshape(Y.shape[0],1)
    X1 = test_df.drop(['days_to_death','bcr_patient_barcode'], axis = 1)
    X1 = np.asarray(X1)
    X1 = X1.reshape(X1.shape[0],X1.shape[1],1)

    X2 = []
    test_imgs = tf.io.gfile.listdir(TEST_DATA_IMG)
    for each_img in test_imgs:
        ds = cv2.imread(TEST_DATA_IMG + each_img, cv2.IMREAD_GRAYSCALE)
        X2.append(ds)
    X2 = np.asarray(X2)
    X2 = X2.reshape(X2.shape[0],X2.shape[1],X2.shape[2],1)

    model = tf.keras.models.load_model(export_path)

    preds = model.predict([X2,X1])

    mae = mean_absolute_error(Y, preds)
    r2 = r2_score(Y, preds)
    mse = mean_squared_error(Y, preds)

    print("MSE: ",mse,', MAE: ', mae, ", R2: ", r2)
