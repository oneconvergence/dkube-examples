#!/usr/bin/env python
# coding: utf-8

# In[3]:


# In[4]:
import os
import configparser
import pandas as pd
from deltalake import DeltaTable


config = configparser.ConfigParser()
config.read("/mnt/deltalake/deltalake.conf")

if config["DEFAULT"]["TABLE_SOURCE"] == "hostpath":
    prefix = config["DEFAULT"]["TABLE_PATH"]
    user_homedir = os.getenv("DKUBE_USER_STORE")
    path = f'{user_homedir}/{prefix}'
    version = int(config["DEFAULT"]["TABLE_VERSION"])

    dt = DeltaTable(path)
elif config["DEFAULT"]["TABLE_SOURCE"] == "s3":
    prefix = config["DEFAULT"]["TABLE_PATH"]
    region = config["DEFAULT"]["AWS_REGION"]
    access_key = config["DEFAULT"]["AWS_ACCESS_KEY_ID"]
    access_secret = config["DEFAULT"]["AWS_SECRET_ACCESS_KEY"]
    version = int(config["DEFAULT"]["TABLE_VERSION"])

    if access_secret != "":
        storage_options = {"AWS_ACCESS_KEY_ID": access_key, "AWS_SECRET_ACCESS_KEY": access_secret, "AWS_REGION": region}
        dt = DeltaTable(f's3://{prefix}', storage_options=storage_options)
    else:
        #May be the role or ~/.aws/credentials is set
        dt = DeltaTable(f's3://{prefix}')

dt.load_version(version)
print(dt.version())


# In[6]:


df_clean = dt.to_pandas()
from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()

df_clean['term'] = label.fit_transform(df_clean['term'])
df_clean['grade'] = label.fit_transform(df_clean['grade'])
# df_clean['emp_length'] = label.fit_transform(df_clean['emp_length'])
df_clean['home_ownership'] = label.fit_transform(df_clean['home_ownership'])
df_clean['verification_status'] = label.fit_transform(df_clean['verification_status'])
df_clean['pymnt_plan'] = label.fit_transform(df_clean['pymnt_plan'])
df_clean['purpose'] = label.fit_transform(df_clean['purpose'])
df_clean['initial_list_status'] = label.fit_transform(df_clean['initial_list_status'])
df_clean['application_type'] = label.fit_transform(df_clean['application_type'])
df_clean['int_rate'] = label.fit_transform(df_clean['int_rate'])
df_clean['total_pymnt'] = label.fit_transform(df_clean['total_pymnt'])
df_clean['total_pymnt_inv'] = label.fit_transform(df_clean['total_pymnt_inv'])
df_clean['total_rec_prncp'] = label.fit_transform(df_clean['total_rec_prncp'])
df_clean['recoveries']= label.fit_transform(df_clean['recoveries'])
df_clean['collection_recovery_fee']= label.fit_transform(df_clean['collection_recovery_fee'])
df_clean['last_pymnt_amnt']= label.fit_transform(df_clean['last_pymnt_amnt'])

df_clean.head()


# In[7]:


x = df_clean.drop(['loan_status'], axis=1)
y = df_clean['loan_status']

x.head()


# In[8]:


from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np 
import matplotlib.pyplot as plt


coltrans = ColumnTransformer(
    [('one_hot_encoder', OneHotEncoder(categories='auto'), [0,1,2,3,4,5,6,7,8])],        
    remainder = 'passthrough'                               
)


# In[10]:


from sklearn.model_selection import train_test_split
import pandas as pd

xtr, xts, ytr, yts = train_test_split(
    x,
    y,
    test_size = .2,
)

from sklearn.ensemble import RandomForestClassifier
import time

start = time.time()

model = RandomForestClassifier()
model.fit(xtr, ytr)

stop = time.time()
duration = stop-start
print('The training took {:.2f} seconds.'.format(duration))

print("Accuracy =>", round(model.score(xts, yts) * 100, 2), '%')
y_pred = model.predict(xts)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(yts, y_pred)

from sklearn.metrics import ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=model.classes_)
disp.plot()
plt.show()


pd.crosstab(yts, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

from sklearn.metrics import classification_report

target_names = ['Bad Loan', 'Good Loan']
print(classification_report(yts, model.predict(xts), target_names=target_names))

import sklearn.metrics as metrics

# calculate the fpr and tpr for all thresholds of the classification
probs = model.predict_proba(xts)
preds = probs[:,1]

fpr, tpr, threshold = metrics.roc_curve(yts, y_pred)
roc_auc = metrics.auc(fpr, tpr)

# Plotting the ROC curve
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()


# In[ ]:




