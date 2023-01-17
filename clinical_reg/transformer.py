from typing import List, Dict
import argparse
import json
import logging
import numpy as np
import requests
import cv2
import pandas as pd
import base64
import kfserving

DEFAULT_MODEL_NAME = "model"

parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                    help='The name that the model is served under.')
parser.add_argument('--predictor_host', help='The URL for the model predict function', required=True)

args, _ = parser.parse_known_args()

class ImageTransformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host

    def preprocess(self, inputs: Dict) -> Dict:
        #return {'instances': [image_transform(instance) for instance in inputs['instances']]}        
        logging.info("inputs %s", str(inputs))
        del inputs['instances']
        try:
            json_data = inputs
        except ValueError:
            return json.dumps({ "error": "Recieved invalid json" })
        data = json_data["signatures"]["inputs"][0][0]["data"].encode()
        csv = json_data["file"]
        with open("/tmp/image.png", "wb") as fh:
            fh.write(base64.decodebytes(data))
        f = open("/tmp/file.txt", "w")
        f.write(csv)
        f.close()
        test_df = pd.read_csv("/tmp/file.txt")
        csv = test_df.drop(['days_to_death','bcr_patient_barcode'], axis = 1)
        csv = np.asarray(csv)
        csv = csv.reshape(csv.shape[0],csv.shape[1],1)
        img = cv2.imread("/tmp/image.png", cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28,28))
        img = img.reshape(1,img.shape[0],img.shape[1],1)
        payload = {
            "inputs": {'csv_input': csv.tolist(),'img_input': img.tolist()}, "token":inputs['token']
        }
        return payload
    
    def postprocess(self, inputs: List) -> List:
        return inputs

if __name__ == "__main__":
    transformer = ImageTransformer(args.model_name, predictor_host=args.predictor_host)
    kfserver = kfserving.KFServer()
    kfserver.start(models=[transformer])
