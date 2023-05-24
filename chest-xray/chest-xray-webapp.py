# This is a WebApp to test the chest x-ray model.  In order to run:
# pip install streamlit
# streamlit run chest-xray-webapp.py
#
# Use the url identified by the app
# Fill in the fields as requested by the app
# You must have access to the internal url of the DKube instance

import numpy as np
import streamlit as st
import requests
import json
from PIL import Image


st.title("Chest X-Ray Example")

serving_url = st.text_input("DKube Deployment Endpoint URL")
auth_token = st.text_input("Dkube user authentication token")


uploaded_file = st.file_uploader("Upload Image ",type=["jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = image.resize((200,200))
    img_array = np.array(image)
    img_array = img_array.reshape(1,200,200, 1)
    print(img_array.shape)

if st.button('Predict'): 
    payload = {
            "inputs": {'input_1': img_array.tolist()}
        }
    r = requests.post(serving_url, json=payload, headers = {'authorization': "Bearer " + auth_token}, verify = False)
    prediction = json.loads(r.content.decode('utf-8'))
    if "outputs" in prediction:
        preds = prediction["outputs"][0]
        if preds[0] > preds[1]:
            st.success("Normal")
        else:
            st.success("Pneumonia")
    else:
        st.error(prediction)
