import pickle
import numpy as np
import streamlit as st
import requests
import pandas as pd
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
import time

st.title("DKube Deltalake Example Prediction test webapp")
st.header("Sends prediction requests as kafka messages to delta lake model deployed in DKube platform")


# Input fields
kafka_broker = st.text_input("Kafka broker endpoint")
kafka_topic = st.text_input("Kafka topic")
testdata_version = st.selectbox("Select version of test data to be sent to predictor", ("version2", "version1"))
count = st.text_input("Number of times to send test data to predictor")


class KafkaMessenger:
    def __init__(self, broker, nreqs):
        self.broker = broker
        self.nreqs = nreqs

    def producer(self, topic, msg):
        self.producer = KafkaProducer(
                bootstrap_servers=self.broker,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries = 3
            )
        nreqs = self.nreqs
        string = f"Sending [{nreqs}] pred requests to kafka broker on topic [{topic}] ...."
        st.write(string)
        my_bar = st.progress(0)
        for i in range(nreqs):
            try:
                future = self.producer.send(topic,msg)
                self.producer.flush()
                future.get(timeout=60)
                percent = int(( (i+1) * 100 ) / nreqs)
                #st.write(f"{percent}:{i}")
                my_bar.progress(percent)
            except Exception as ex:
                return ex
            time.sleep(0.1)
        return {'status_code':200, 'error':None}

    def consumer(self, topic):
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(topic,
                             group_id='training',
                             bootstrap_servers=[self.broker],
                             consumer_timeout_ms=60000)
        counter = 0
        for message in consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                  message.offset, message.key,
                                                  message.value))
            respmsg = message.value.decode()
            jresp = json.loads(respmsg)
            if jresp[0] == 1:
                st.write(f"Resp [{counter}] > :+1: (Good Loan)")
            else:
                st.write(f"Resp [{counter}] > :-1: (Bad Loan)")

            #st.write(message.value)
            counter += 1
            if counter >= self.nreqs:
                break

if st.button('Predict'):
    data = {"instances": [[1, 1, 0, 2, 0, 2, 0, 0, 36498, 36215, 6838, 0, 0, 33543, 54, 8313], [0, 2, 4, 2, 0, 13, 0, 0, 14370, 15181, 4601, 0, 0, 7657, 175, 7560]]}
    kf = KafkaMessenger(kafka_broker, int(count))
    kf.producer(kafka_topic, data)

    kafka_resptopic = kafka_topic + "-resp"
    string = f"Waiting for predictions on kafka topic {kafka_resptopic}"
    #st.write(string)

    with st.spinner(string):
        kf.consumer(kafka_resptopic)

    st.success("done")
