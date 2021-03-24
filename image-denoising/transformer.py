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
import torch
import torchvision
import matplotlib.pyplot as plt

DEFAULT_MODEL_NAME = "model"

parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                    help='The name that the model is served under.')
parser.add_argument('--predictor_host', help='The URL for the model predict function', required=True)

args, _ = parser.parse_known_args()

filename = '/tmp/temp.png'
meanTorch = 825.9008412551716
stdTorch = 463.53995615631595

def b64_filewriter(filename, content):
    string = content.encode('utf8')
    b64_decode = base64.decodebytes(string)
    fp = open(filename, "wb")
    fp.write(b64_decode)
    fp.close()

def imgToTensor(img):
    '''
    Convert a 2D single channel image to a pytorch tensor.
    '''
    img.shape=(img.shape[0],img.shape[1],1)
    imgOut = torchvision.transforms.functional.to_tensor(img.astype(np.float32))
    return imgOut

class ImageTransformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host

    def preprocess(self, inputs: Dict) -> Dict:
        logging.info("preprocess1")
        del inputs['instances']
        try:
            json_data = inputs
        except ValueError:
            return json.dumps({ "error": "Recieved invalid json" })
        data = json_data["signatures"]["inputs"][0][0]["data"]
        b64_filewriter(filename, data)
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        inputs_raw= torch.zeros(1,1,img.shape[0],img.shape[1])
        inputs_raw[0,:,:,:]=imgToTensor(img)
        model_inputs = (inputs_raw-meanTorch)/stdTorch
        payload = {"instances": model_inputs.tolist(), "token":inputs["token"]}
        logging.info("token =======> %s",str(inputs["token"]))
        return payload

    def postprocess(self, predictions: List) -> List:
        output = torch.tensor(predictions['predictions'])
        samples = (output).permute(1, 0, 2, 3)*10.0 #We found that this factor can speed up training
        samples = samples * stdTorch + meanTorch
        means = torch.mean(samples,dim=0,keepdim=True)[0,...] # Sum up over all samples
        means=means.cpu().detach().numpy()
        means.shape=(output.shape[2],output.shape[3])
        plt.imsave('/tmp/out.png',means)
        with open('/tmp/out.png', 'rb') as open_file:
            byte_content = open_file.read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode('utf-8')
        logging.info("prep =======> %s",str(means.shape))
        return {'image':base64_string, 'p_class': ""}

if __name__ == "__main__":
    transformer = ImageTransformer(args.model_name, predictor_host=args.predictor_host)
    kfserver = kfserving.KFServer()
    kfserver.start(models=[transformer])
