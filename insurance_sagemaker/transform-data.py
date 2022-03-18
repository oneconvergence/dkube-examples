import logging
import sys, json
import os
import pandas as pd
from sklearn import preprocessing

DEFAULT_MODEL_NAME = "model"
class Transformer():
    def preprocess(self, dataframe):
        data_to_preprocess = dataframe 
        for col in ['sex', 'smoker', 'region']:
            if (data_to_preprocess[col].dtype == 'object'):
                le = preprocessing.LabelEncoder()
                le = le.fit(data_to_preprocess[col])
                data_to_preprocess[col] = le.transform(data_to_preprocess[col])
                print('Completed Label encoding on',col)
        preprocessed_data = data_to_preprocess
        return preprocessed_data

    def postprocess(self, dataframe):
        pass

