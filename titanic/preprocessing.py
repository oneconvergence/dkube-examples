import os
import json
import glob
import boto3
import argparse
import pymysql
import pandas as pd
import requests
from sqlalchemy import create_engine

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_source", dest="data_source", default='local', type=str, help="source of the dataset")
    parser.add_argument("--train_type", dest="train_type", default='training', type=str, help="training or retraining")
    parser.add_argument("--monitor_name", dest="monitor_name", default='mm-demo', type=str, help="modelmonitor name")
    parser.add_argument("--user",dest="user",type=str,help="dkube user name")

    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    data_source =   FLAGS.data_source
    input_train_type = FLAGS.train_type
    mm_name = FLAGS.monitor_name
    user = FLAGS.user
    
    DATA_DIR = '/data'
    
    ### SQL DATASOURCE ###
    if data_source == "sql":  
        with open(DATA_DIR+'/sql.conf') as json_file:
            sql_config = json.load(json_file)

        hostname = str(sql_config["sql_host"])
        username=sql_config["sql_user"]
        databasename=sql_config["sql_database"]

        datum_name = "titanic-data-sql"
        headers={"authorization": "Bearer "+os.getenv("DKUBE_USER_ACCESS_TOKEN")}
        url = "http://dkube-controller-worker.dkube:5000/dkube/v2/controller/users/%s/datums/class/dataset/datum/%s"
        resp = requests.get(url % (user, datum_name), headers=headers).json()
        password = resp['data']['datum']['sql']['password']

        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=databasename, user=username, pw=password))
        
        if input_train_type == 'training':
            query = "SELECT * FROM titanic"
            train_df = pd.read_sql(query, engine)
            train_df.to_csv('/train-data/data.csv',index=False)
        
        if input_train_type == 'retraining':
            query = "SELECT * FROM titanic_gt"
            train_df = pd.read_sql(query, engine)
            train_df.rename(columns={'GT_Survival':'Survival'}, inplace=True)
            train_df.to_csv('/train-data/data.csv',index=False)
    
    ### AWS-S3 DATASOURCE ###
    if data_source == "aws_s3":
        if input_train_type == 'training':
            data = pd.read_csv(DATA_DIR+'/titanic.csv')
            data.to_csv('/train-data/data.csv',index=False)
        
        if input_train_type == 'retraining':
            config = json.load(open(os.path.join(DATA_DIR, "config.json")))
            with open(os.path.join(DATA_DIR, "credentials"), "r") as f:
                creds = f.read()
            access_key = creds.split("\n")[1].split("=")[-1].strip()
            secret_key = creds.split("\n")[2].split("=")[-1].strip()

            session = boto3.session.Session()
            s3_client = boto3.resource(
                service_name="s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)


            my_bucket = s3_client.Bucket(config["Bucket"])

            for s3_object in my_bucket.objects.all():
                if s3_object.key.startswith(mm_name+'/groundtruth'):
                    path, filename = os.path.split(s3_object.key)
                    if filename.endswith('GTpredict_data.csv'):
                        my_bucket.download_file(s3_object.key, filename)
               
                final_df = pd.DataFrame()
                for file in glob.glob("*GTpredict_data.csv"):
                    data = pd.read_csv(file)
                    final_df = pd.concat([final_df,data])

                final_df.rename(columns={'GT_Survival':'Survival'}, inplace=True)
                final_df.to_csv('/train-data/data.csv',index=False)
            

                
   ### LOCAL DATA SOURCE #####          
    if data_source == 'local':
        if input_train_type == 'training':
            data = pd.read_csv(DATA_DIR+'/titanic.csv')
            data.to_csv('/train-data/data.csv',index=False)
        
        if input_train_type == 'retraining':
            final_df = pd.DataFrame()
            for file in glob.glob(os.path.join(DATA_DIR, "*.csv")):
                data = pd.read_csv(file)
                final_df = pd.concat([final_df,data])

            final_df.rename(columns={'GT_Survival':'Survival'}, inplace=True)
            final_df.to_csv('/train-data/data.csv',index=False)
