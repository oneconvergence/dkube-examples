from typing import List, Dict
import kfserving
import json
import logging
import argparse
import numpy as np
import requests
import cv2
import pandas as pd
import base64

DEFAULT_MODEL_NAME = "model"

parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                    help='The name that the model is served under.')
parser.add_argument('--predictor_host', help='The URL for the model predict function', required=True)

args, _ = parser.parse_known_args()

class Transformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host

    def preprocess(self, inputs: Dict) -> Dict:
        logging.info("inputs %s", str(inputs))
        del inputs['instances']
        try:
            json_data = inputs
        except ValueError:
            return json.dumps({ "error": "Recieved invalid json" })
        data = json_data["signatures"]["inputs"][0][0]["data"].encode()
        with open("image.png", "wb") as fh:
            fh.write(base64.decodebytes(data))
        img = cv2.imread("image.png", cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28,28))
        img = img.reshape(1,1,img.shape[0],img.shape[1])
        img = img.astype('float32')
        payload = {"instances": img.tolist(), "token":inputs["token"]}
        return payload

    def postprocess(self, inputs: List) -> List:
        print ("postprocess", inputs, flush=True)
        inputs["prediction"] = np.argmax(inputs["prediction"][0])
        return inputs

if __name__ == "__main__":
    transformer = Transformer(args.model_name, predictor_host=args.predictor_host)
    kfserver = kfserving.KFServer()
    kfserver.start(models=[transformer])