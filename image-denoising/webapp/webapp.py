import pickle
import numpy as np
import streamlit as st
import requests
import pandas as pd
import json

import base64
from PIL import Image


st.title("Image Denoising Example")

serving_url = st.text_input("Dkube serving URL")
auth_token = st.text_input("Dkube user authentication token")


uploaded_file = st.file_uploader("Upload Image ",type=["png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    data = Image.fromarray(img_array)
    data.save('img.png') 
    with open('img.png', "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')


if st.button('Predict'): 
    payload = {
            'signatures':{
                'inputs':[[{'data': encoded_string}]]
            },
            'instances': [],
            'token': auth_token
        }
    r = requests.post(serving_url, json=payload, headers = {'authorization': "Bearer " + auth_token}, verify = False)
    prediction = json.loads(r.content.decode('utf-8'))
    imgdata = prediction['image']
    with open("output_image.png", "wb") as fh:
        fh.write(base64.b64decode(imgdata))
        st.image("output_image.png", width=None)

