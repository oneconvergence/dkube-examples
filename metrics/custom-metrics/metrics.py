import json
import math,sys,time
import random
import requests
import datetime
import shutil

print("*******************Custom Metrics Generator***************************")

# Metrics file path is fixed. Write to this location.
METRICS_FILE="/tmp/metrics.json"


metric_value = random.random()

def get_timestamp():
    timestamp = int(time.time())
    return timestamp

metrics = dict()
metrics['timestamp'] = get_timestamp()
metrics['mse'] = random.randrange(100000000, 150000000, 5) 
metrics['mae'] = random.randrange(5000, 15000, 5)
metrics['rmse'] = random.randrange(8000, 15000, 5)
metrics['mape'] = round(random.uniform(0,1), 2)
metrics['r2_score'] = round(random.uniform(0,1), 2)
metrics['samples'] = random.randrange(0, 200, 5)

formatted_metrics = json.dumps(metrics, indent=4) 
with open(METRICS_FILE, "w") as f:
   f.write(formatted_metrics)
   f.flush()

print(formatted_metrics)
#shutil.make_archive('/tmp/metrics.json', 'tar', '/tmp/', 'metrics.json')

sys.exit(0)
