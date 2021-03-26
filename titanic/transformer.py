import json
import numpy as np
import requests
import kfserving
import argparse
from typing import List, Dict
import logging
import io
import base64
import sys, json
import os
import pandas as pd
from io import StringIO
import pickle
from preprocess import transform_features, features

DEFAULT_MODEL_NAME = "model"

parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
parser.add_argument(
    "--model_name",
    default=DEFAULT_MODEL_NAME,
    help="The name that the model is served under.",
)
parser.add_argument(
    "--predictor_host", help="The URL for the model predict function", required=True
)

args, _ = parser.parse_known_args()

class Transformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host
        dirpath = os.path.dirname(os.path.realpath(__file__))
        self.encoders = pickle.load( open( dirpath + "/encoders.pkl", "rb" ) )

    def preprocess(self, inputs: Dict) -> Dict:
        # inputs is a json file, inside that data, using the data value form a image
        # write into jpeg file
        del inputs["instances"]
        logging.info("prep =======> %s", str(type(inputs)))
        try:
            json_data = inputs
        except ValueError:
            return json.dumps({"error": "Recieved invalid json"})
        data = json_data["signatures"]["inputs"][0][0]["data"]
        df = pd.read_csv(StringIO(data))
        df = transform_features (df)
        for feature in features:
            le = self.encoders[feature]
            df[feature] = le.transform(df[feature])

        values = df.drop(["Survived", "PassengerId"], 1, errors='ignore').values
        payload = {"instances": values.tolist(), "token": inputs["token"]}
        return payload

    def postprocess(self, predictions: List) -> List:
        logging.info("postprocess =======> %s", str(type(predictions)))
        predictions = ["Dead" if pred == 0 else "Alive" for pred in predictions["predictions"]]
        return {"result": predictions}

if __name__ == "__main__":
    transformer = Transformer(args.model_name, predictor_host=args.predictor_host)
    kfserver = kfserving.KFServer()
    kfserver.start(models=[transformer])
