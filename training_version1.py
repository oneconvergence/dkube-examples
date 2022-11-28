import os
import configparser
import pandas as pd
from deltalake import DeltaTable
import sklearn.metrics as metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, roc_curve

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

import joblib
import numpy as np 
import mlflow.sklearn
import urllib3
import json
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def training():
    config = configparser.ConfigParser()
    config.read("/mnt/deltalake/deltalake.ini")

    if config["DEFAULT"]["TABLE_SOURCE"] == "hostpath":
        prefix = config["DEFAULT"]["TABLE_PATH"]
        user_homedir = os.getenv("DKUBE_USER_STORE")
        path = f'{user_homedir}/{prefix}'
        version = int(config["DEFAULT"]["TABLE_VERSION"])

        dt = DeltaTable(path)
    elif config["DEFAULT"]["TABLE_SOURCE"] == "s3":
        prefix = config["DEFAULT"]["TABLE_PATH"]
        region = config["DEFAULT"]["AWS_REGION"]
        access_key = config["DEFAULT"].get("AWS_ACCESS_KEY_ID", "")
        access_secret = config["DEFAULT"].get("AWS_SECRET_ACCESS_KEY", "")
        version = int(config["DEFAULT"]["TABLE_VERSION"])

        if access_secret != "":
            storage_options = {"AWS_ACCESS_KEY_ID": access_key, "AWS_SECRET_ACCESS_KEY": access_secret, "AWS_REGION": region}
            dt = DeltaTable(f's3://{prefix}', storage_options=storage_options)
        else:
            #May be the role or ~/.aws/credentials is set
            storage_options = {"AWS_REGION": region}
            dt = DeltaTable(f's3://{prefix}', storage_options=storage_options)

    dt.load_version(version)
    print("Loaded verion => ", dt.version())

    df_clean = dt.to_pandas()
    label = LabelEncoder()

    print("Features =>", list(df_clean.columns))

    print("\n")
    print(df_clean.head())
    print("\n")

    df_clean['term'] = label.fit_transform(df_clean['term'])
    df_clean['grade'] = label.fit_transform(df_clean['grade'])
    df_clean['int_rate'] = label.fit_transform(df_clean['int_rate'])
    df_clean['verification_status'] = label.fit_transform(df_clean['verification_status'])


    x = df_clean.drop(['loan_status'], axis=1)
    y = df_clean['loan_status']


    coltrans = ColumnTransformer(
        [('one_hot_encoder', OneHotEncoder(categories='auto'), [0,3,5])],      # 0,3,5 refers to the column indexes that need to be transformed      
        remainder = 'passthrough'                               
    )                                                         

    x = np.array(coltrans.fit_transform(x))

    xtr, xts, ytr, yts = train_test_split(
        x,
        y,
        test_size = .2
    )


    print(ytr.value_counts())
    print(yts.value_counts())

    xtr_2 = xtr
    ytr_2 = ytr

    start = time.time()

    with mlflow.start_run(run_name="dl-loan") as run:
        model = RandomForestClassifier()
        model.fit(xtr_2, ytr_2)

        mlflow.sklearn.log_model(model, "badloan-classifier")

        stop = time.time()
        duration = stop-start
        print('The training took {:.2f} seconds.'.format(duration))
        print("Accuracy =>", round(model.score(xts, yts) * 100, 2), '%')

        y_pred = model.predict(xts)


        cm = confusion_matrix(yts, y_pred)

        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                       display_labels=model.classes_)
        disp.plot()
        plt.show()
        plt.savefig('cm.png')

        pd.crosstab(yts, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

        target_names = ['Bad Loan', 'Good Loan']
        class_report = classification_report(yts, model.predict(xts), target_names=target_names)
        print(class_report)


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
        plt.savefig('roc.png')

        acc = accuracy_score(yts, y_pred)
        precision = precision_score(yts, y_pred)
        roc = metrics.roc_auc_score(yts, y_pred)
        # confusion matrix values
        tp = cm[0][0]
        tn = cm[1][1]
        fp = cm[0][1]
        fn = cm[1][0]        

        # get classification metrics
        class_report = classification_report(yts, y_pred, output_dict=True)
        recall_0 = class_report['0']['recall']
        f1_score_0 = class_report['0']['f1-score']
        recall_1 = class_report['1']['recall']
        f1_score_1 = class_report['1']['f1-score']

        # log metrics in mlflow
        mlflow.log_metric("accuracy_score", acc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("true_positive", tp)
        mlflow.log_metric("true_negative", tn)
        mlflow.log_metric("false_positive", fp)
        mlflow.log_metric("false_negative", fn)
        mlflow.log_metric("recall_0", recall_0)
        mlflow.log_metric("f1_score_0", f1_score_0)
        mlflow.log_metric("recall_1", recall_1)
        mlflow.log_metric("f1_score_1", f1_score_1)
        mlflow.log_metric("roc", roc)

        mlflow.log_artifact('cm.png', "confusion-matrix")
        mlflow.log_artifact('roc.png', "roc-auc-plots")

    joblib.dump(model, '/mnt/model/model.joblib')

    loaded_model = joblib.load("/mnt/model/model.joblib")
    print(round(loaded_model.score(xts, yts) * 100, 2), '%')
    sampled = np.resize(xts.tolist(), (2,17))
    with open("testdata_v1.json", "w+") as f:
        f.write(json.dumps(sampled.tolist()))
    pred = loaded_model.predict(sampled)
    print("joblib loaded model prediction =>",pred)

if __name__ == '__main__':
    training()
