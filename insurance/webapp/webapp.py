import pickle
import numpy as np
import streamlit as st
import requests
import pandas as pd
import json


st.title("Predict insurance charges")
st.header("Calculating the insurance charges that could be charged by an insurer based on a person's attributes")

def load_data():
    df = pd.DataFrame({'sex': ['Male','Female'],
                       'smoker': ['Yes', 'No']}) 
    return df
df = load_data()

def load_data1():
    df1 = pd.DataFrame({'region' : ['southeast' ,'northwest' ,'southwest' ,'northeast']}) 
    return df1
df1 = load_data1()

# Data input feilds
serving_url = st.text_input("Dkube serving URL")
auth_token = st.text_input("Dkube user auth token")
sex = st.selectbox("Select Sex", df['sex'].unique())
smoker = st.selectbox("Are you a smoker", df['smoker'].unique())
region = st.selectbox("Which region do you belong to?", df1['region'].unique())
age = st.slider("What is your age?", 18, 100)
bmi = st.slider("What is your bmi?", 10, 60)
children = st.slider("Number of children", 0, 10)

# converting text input to numeric to get back predictions from backend model.
if sex == 'male':
    gender = 1
else:
    gender = 0
    
if smoker == 'yes':
    smoke = 1
else:
    smoke = 0
    
if region == 'southeast':
    reg = 2
elif region == 'northwest':
    reg = 3
elif region == 'southwest':
    reg = 1
else:
    reg = 0
    

# store the inputs
features = {'age':age,'sex':gender,'bmi':bmi,'children':children,'smoker':smoke,'region':reg}
df = pd.DataFrame(features, index=[0]) 
# convert user inputs into an array fr the model

final_features = df.values


if st.button('Predict'):           # when the submit button is pressed
    payload = {
            'signatures':{
                'inputs':[[{'data':df.to_csv(index=False)}]]
            },
            'instances': [],
            'token': auth_token
        }
    r = requests.post(serving_url, json=payload, headers = {'authorization': "Bearer " + auth_token}, verify = False)
    prediction = json.loads(r.content.decode('utf-8'))
    st.success(prediction["result"])
