import argparse
import json

import numpy as np
import requests
import tensorflow as tf
import cv2
import pandas as pd

DATA_DIR = 'data_splits/'
TEST_DATA_CLI = DATA_DIR + 'test/CLI/'
TEST_DATA_IMG = DATA_DIR + 'test/IMG/'
TEST_DATA_RNA = DATA_DIR + 'test/RNA/'

test_df = pd.read_csv(TEST_DATA_CLI + "cli_data_processed_test.csv")
X1_test = test_df.drop(['days_to_death','bcr_patient_barcode'], axis = 1)
X1_test = np.asarray(X1_test)
X1_test = X1_test.reshape(X1_test.shape[0],X1_test.shape[1],1)

X2_test = []
test_imgs = tf.io.gfile.listdir(TEST_DATA_IMG)
for each_img in test_imgs:
    ds = cv2.imread(TEST_DATA_IMG + each_img, cv2.IMREAD_GRAYSCALE)
    X2_test.append(ds)
X2_test = np.asarray(X2_test)
X2_test = X2_test.reshape(X2_test.shape[0],X2_test.shape[1],X2_test.shape[2],1)

## Generating random number to pick random saple from test set. 
idx = np.random.randint(1,len(X1_test))

img = X2_test[idx]
img = img.reshape(1,img.shape[0], img.shape[1],1)

csv = X1_test[idx]
csv = csv.reshape(1,csv.shape[0],1)

payload = {
    "inputs": {'csv_input:0': csv.tolist(),'img_input:0': img.tolist()}
}

URL = 'http://localhost:9000/v1/models/regressmodel'

r = requests.post(URL + ':predict', json=payload)

pred = json.loads(r.content.decode('utf-8'))

print(pred)

'''
################################ Launch Server ################################
tensorflow_model_server \ 
--model_base_path=/home/ritesh/Desktop/CPTAC-GBM/clinical/model/infer_model \ 
--rest_api_port=9000 --model_name=regressmodel
'''