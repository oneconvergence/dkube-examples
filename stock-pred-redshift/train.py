import numpy as np
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import csv, sys, requests
import matplotlib.pyplot as plt
from tensorboard_logger import configure, log_value, log_histogram, log_images,  Logger
from PIL import Image
import cv2, os, json, re
import joblib, psycopg2
import requests


r_endpoint = os.getenv('DKUBE_DATASET_REDSHIFT_ENDPOINT', None)
r_database = os.getenv('DKUBE_DATASET_REDSHIFT_DATABASE', None)
r_user = os.getenv('DKUBE_DATASET_REDSHIFT_USER', None)


if 'https:' in r_endpoint:
    p = '(?:https*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p,r_endpoint)
else:
    p = '(?:http*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p,r_endpoint)


dates = []
prices = []
name = str(sys.argv[1]) if len(sys.argv) > 1 else 'SVM for stock Preiction'
kernel = str(sys.argv[2]) if len(sys.argv) > 2 else 'rbf'
C = float(sys.argv[3]) if len(sys.argv) > 3 else 1e3
gamma = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
degree= int(sys.argv[5]) if len(sys.argv) > 5 else 2

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def rs_fetch_datasets():
    user = os.getenv("DKUBE_USER_LOGIN_NAME")
    url = "http://dkube-controller-worker.dkube:5000/dkube/v2/controller/users/%s/datums/class/dataset/datum/%s"
    headers={"authorization": "Bearer "+os.getenv("DKUBE_USER_ACCESS_TOKEN")}
    datasets = []
    for ds in json.load(open('/etc/dkube/redshift.json')):
        resp = requests.get(url % (user, ds.get('rs_name')), headers=headers).json()
        ds['rs_password'] = resp['data']['datum']['redshift']['password']
        datasets.append(ds)
    return datasets

def get_password(user, db):
    datasets = rs_fetch_datasets()
    for dataset in datasets:
        if dataset.get("rs_user") == user and dataset.get("rs_database") == db:
            return dataset.get("rs_password")
    raise Exception("Failed to find password for DB {} with User {}".format(user, db))

MODEL_DIR = '/opt/dkube/model'

def log_metrics(key, value):
    url = "http://dkube-exporter.dkube:9401/mlflow-exporter"
    train_metrics = {}
    train_metrics['mode']="train"
    train_metrics['key'] = key
    train_metrics['value'] = value
    train_metrics['epoch'] = 1
    train_metrics['step'] = 1
    train_metrics['jobid']=os.getenv('DKUBE_JOB_ID')
    train_metrics['run_id']=os.getenv('DKUBE_JOB_UUID')
    train_metrics['username']=os.getenv('DKUBE_USER_LOGIN_NAME')
    requests.post(url, json = train_metrics)

def load_rs_to_csv(usr,passwd, hst, prt, db):
    try:
        connection = psycopg2.connect(user = usr,
       	                              password = passwd,
           	                          host = hst,
               	                      port = prt,
                   	                  database = db)
    except (Exception, psycopg2.Error) as error :
        print("Error while connecting to Redshift", error)

    wf = open('goog.csv', mode='w')
    csv_writer = csv.writer(wf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Date','Open','High','Low','Close','Volume'])

    cursor = connection.cursor()
    cursor.execute("SELECT * from sklearn;")
    record = cursor.fetchall()
    for each in record:
        csv_writer.writerow(each)

def get_data(filename):
	with open(filename, 'r') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)	# skipping column names
		for row in csvFileReader:
			dates.append(int(row[0].split('-')[0]))
			prices.append(float(row[1]))
	return

if not os.path.exists(MODEL_DIR + "/logs/SVMrun"):
    os.makedirs(MODEL_DIR + "/logs/SVMrun")

configure(MODEL_DIR + "/logs/SVMrun", flush_secs=5)

if __name__ == "__main__":

    r_password = get_password(r_user, r_database)

    load_rs_to_csv(r_user, r_password, m.group('host'), m.group('port'), r_database)

    get_data('goog.csv')

    dates = np.reshape(dates,(len(dates), 1))

    svm = SVR(kernel= kernel, C= C, degree= degree, gamma=gamma)

    svm.fit(dates, prices)

    predictions = svm.predict(dates)

    (rmse, mae, r2) = eval_metrics(prices, predictions)
    
    #Dkube UI logging
    log_metrics('RMSE', rmse)
    log_metrics('MAE', mae)
    log_metrics('R2', r2)
    
    filename = MODEL_DIR + '/model.joblib'
    joblib.dump(svm, filename)

    plt.plot(dates, prices, color= 'black', label = "Data", marker = '*')
    plt.plot(dates,predictions, color= 'red', label = "Predictions", marker = 'o')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('SVM predictions with '+kernel+ ' kernel')
    plt.legend()
    plt.savefig('svm.png')
    
    #Tensorboard logging
    log_value('RMSE', rmse)
    log_value('MAE', mae)
    log_value('R2', r2)

    img = cv2.imread('svm.png')
    log_histogram('Stock Prices', prices, step=1)
    log_images('Stock Predictions Graph',[img])