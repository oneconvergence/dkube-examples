import json
import math,sys,time
import random
import requests
import datetime

print("*******************Custom Metrics Generator***************************")
url = "http://dkube-exporter.dkube:9401/modelmonitor/metrics"

monitor_id = sys.argv[1]
print("monitor id is ",monitor_id)

metric_value = random.random()

payload = json.dumps({
  "id": monitor_id,
  "timestamp": math.ceil(datetime.datetime.utcnow().timestamp()),
"metrics": [
    {        "label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f","mm_feature":"age"},
            "metric_name": "pval",
            "type": "data_drift",
            "generated_value":0.0
    },
    {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f","mm_feature":"bmi"},
       "metric_name": "pval",
       "type": "data_drift",
       "generated_value": 0.189
    },
    {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f","mm_feature":"smoker"},
       "metric_name": "pval",
       "type": "data_drift",
       "generated_value": 0.0},
    {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f"}, 
       "metric_name": "accuracy", 
       "type": "performance_drift", 
       "generated_value": 1.0},
      {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f"}, 
       "metric_name": "precision", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f"}, 
       "metric_name": "recall", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f"}, 
       "metric_name": "f1_score", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f"}, 
       "metric_name": "jaccard_score", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": "c07a61a4-f660-4a7f-84e1-05f7330e748f"}, 
       "metric_name": "roc_auc_score", 
       "type": "performance_drift", 
       "generated_value": metric_value}
]})
headers = {
  'Content-Type': 'application/json',
  'Authorization': "Bearer "
}
response = requests.request("POST", url, headers=headers, data=payload)
print("response is ",response)
