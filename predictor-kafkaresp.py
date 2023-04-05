import kfserving
import joblib
import numpy as np
import os
from typing import List, Dict
import argparse

JOBLIB_FILE = "model.joblib"

from kafka import KafkaProducer
import json

class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
                bootstrap_servers=self.broker,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries = 3
            )

    def send_msg(self, msg):
        print("sending message...")
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex

class SKLearnModel(kfserving.KFModel): #pylint:disable=c-extension-no-member
    def __init__(self, name: str, model_dir: str):
        super().__init__(name)
        self.name = name
        self.model_dir = model_dir
        self.ready = False

    def load(self):
        model_file = os.path.join(kfserving.Storage.download(self.model_dir), JOBLIB_FILE) #pylint:disable=c-extension-no-member
        self._joblib = joblib.load(model_file) #pylint:disable=attribute-defined-outside-init
        self.ready = True

    def predict(self, request: Dict) -> Dict:
        instances = request["instances"]
        try:
            inputs = np.array(instances)
        except Exception as e:
            raise Exception(
                "Failed to initialize NumPy array from inputs: %s, %s" % (e, instances))
        try:
            result = self._joblib.predict(inputs).tolist()
            reqtopic = os.getenv("DKUBE_USER_LOGIN_NAME")
            resptopic = reqtopic + "-resp"
            broker = "dkube-kafka-cp-kafka-headless.dkube-kafka:9092"
            message_producer = MessageProducer(broker,resptopic)
            resp = message_producer.send_msg(result)
            print(f"Sent prediction result to {broker} on topic {resptopic}")
            print(resp)
            return { "predictions" : result }
        except Exception as e:
            raise Exception("Failed to predict %s" % e)



DEFAULT_MODEL_NAME = "model"
DEFAULT_LOCAL_MODEL_DIR = "/tmp/model"

parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
parser.add_argument('--model_dir', required=True,
                    help='A URI pointer to the model binary')
parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                    help='The name that the model is served under.')
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    #hardcoding to work with latest kubeflow release
    model = SKLearnModel(args.model_name, "/opt/ml/model")
    model.load()
    kfserving.KFServer().start([model])
