import json
import math,os,time
import random
import requests
import datetime

print("*******************Custom Metrics Generator***************************")
url = "http://dkube-exporter.dkube:9401/modelmonitor/metrics"
monitor_id = os.getenv("MM_ID")
run_id = os.getenv("MM_RUNID")
performance_frequency = 0
with open(os.getenv("MM_CONFIG_FILE")) as f:
    configuration = json.load(f)
    if configuration:
        drift_monitoring = configuration.get("performance_monitoring")
        performance_frequency = drift_monitoring.get("frequency", 0)
    
if not performance_frequency: 
    exit(f"performance frequency is {performance_frequency}, it should be greater than 5 minutes")

def get_timestamp():
    run_end_time = int(time.time())
    run_freq = performance_frequency * 60
    run_end_time = run_end_time - (run_end_time % run_freq )
    return run_end_time

    

metric_value = random.random()
payload = json.dumps({
  "id": monitor_id,
  "timestamp": get_timestamp(),
"metrics": [
      {"label_values": {"run_id": run_id}, 
       "metric_name": "accuracy", 
       "type": "performance_drift", 
       "generated_value": metric_value},
      {"label_values": {"run_id": run_id}, 
       "metric_name": "precision", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id":run_id}, 
       "metric_name": "recall", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": run_id}, 
       "metric_name": "f1_score", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": run_id}, 
       "metric_name": "jaccard_score", 
       "type": "performance_drift", 
       "generated_value": metric_value}, 
      {"label_values": {"run_id": run_id}, 
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
