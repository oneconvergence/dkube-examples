import json
import math,sys,time
import random
import datetime

print("*******************Custom Metrics Generator***************************")

# Metrics file path is fixed. Write to this location.
METRICS_FILE="/tmp/metrics.json"

# It should be written as a list of objects.
# Example: [ { "timestamp": 1651895701, "metric1":2 } ]
# timestamp is in sec from epoch
# Note: List is limited to 1 entry in 3.3 release
metrics_list = list()

def get_timestamp():
    timestamp = int(time.time())
    return timestamp


def compute_metrics():
    # Add your logic here
    metrics = dict()
    metrics['timestamp'] = get_timestamp()
    metrics['mse'] = random.randrange(100000000, 150000000, 5) 
    metrics['mae'] = random.randrange(5000, 15000, 5)
    metrics['rmse'] = random.randrange(8000, 15000, 5)
    metrics['mape'] = round(random.uniform(0,1), 2)
    metrics['r2_score'] = round(random.uniform(0,1), 2)
    metrics['samples'] = random.randrange(0, 200, 5)
    metrics_list.append(metrics)

if __name__ == "__main__":
   
    compute_metrics()
    formatted_metrics_list = json.dumps(metrics_list) 
    with open(METRICS_FILE, "w") as f:
        f.write(formatted_metrics_list)
        f.flush()

    print(formatted_metrics_list)

    sys.exit(0)
