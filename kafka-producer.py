#pip install kafka-python
#This producer sends kafka messages over an internal kafka broker deployed in dkube-kafka namespace
#This sends the test data which works with version2 of the deltalake model
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

message_producer = MessageProducer("dkube-kafka-cp-kafka-headless.dkube-kafka:9092","loanreq")
data = {"instances": [[1, 1, 0, 2, 0, 2, 0, 0, 36498, 36215, 6838, 0, 0, 33543, 54, 8313], [0, 2, 4, 2, 0, 13, 0, 0, 14370, 15181, 4601, 0, 0, 7657, 175, 7560]]}
print(f"Sending data {data} to the kafka broker")
resp = message_producer.send_msg(data)
print(resp)
