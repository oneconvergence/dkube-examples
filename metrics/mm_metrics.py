from pandas.core.frame import DataFrame
import urllib3
from prometheus_api_client.metric_range_df import MetricRangeDataFrame
from prometheus_api_client.metrics_list import MetricsList
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
import argparse
import os,sys
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description='Compute min/max/mean/std on monitoring metrics.')
parser.add_argument('-i', "--id", required=True, help='deployment id')
parser.add_argument('-n', type=int, required=True, help="Use metric data from last N days")
parser.add_argument('-t', dest='type', required=True, choices=['health', 'drift', 'performance'],help="metric type")
parser.add_argument('-r', type=int, default=1, help="compute metric statistics on R day interval ")
parser.add_argument('-s', type=int, default=1, help="metrics sampling period as configured in DKube")
parser.add_argument('-o','--output', type=argparse.FileType('w'), default='-', help="CSV output file")

args = parser.parse_args()

token = os.environ.get("DKUBE_USER_ACCESS_TOKEN")
dkube_url = os.environ.get("DKUBE_URL")

if not token or not dkube_url:
    print("DKUBE_USER_ACCESS_TOKEN and DKUBE_URL env variable needs to be set.")
    sys.exit(-1)
    
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
}
prom = PrometheusConnect(url =f"{dkube_url}/dkube/v2/prometheus/", headers=headers, disable_ssl=True)

end_time = parse_datetime("now")
start_time = end_time - timedelta(days=args.n)
duration = args.s * 2
deployment_id=args.id

queries = {
    "health" : {
        "requests_rate" : f"sum(rate(mm_deployment_predictions_total{{mm_id='{deployment_id}', response_code_class='2xx'}}[{duration}m]))",
        "4xx_requests_rate" : f"sum(rate(mm_deployment_predictions_total{{mm_id='{deployment_id}', response_code_class='4xx'}}[{duration}m]))",
        "5xx_requests_rate" : f"sum(rate(mm_deployment_predictions_total{{mm_id='{deployment_id}', response_code_class='5xx'}}[{duration}m]))",
        "latency" : f"sum(rate(mm_deployment_latency_sum{{mm_id='{deployment_id}'}}[{duration}m])) / sum(rate(mm_deployment_latency_count{{mm_id='{deployment_id}'}}[{duration}m]))",
        "cpu_utilization" : f"sum(rate(mm_deployment_cpu_usage_total{{mm_id='{deployment_id}'}}[{duration}m]))",
        "memory_utilization": f"sum(mm_deployment_memory_usage{{mm_id='{deployment_id}'}})"
    },
    "performance": {}, "drift": {}
}

for metric in ["accuracy", "precision_recall","recall_score","f1_score","jaccard_score","roc_auc_score","mse","mae","mape","rmse","r2_score"]:
    queries["performance"][metric]=f"mm_{metric}{{mm_id='{deployment_id}'}}"

drift_data = prom.get_metric_range_data(metric_name='mm_pval', label_config={"mm_id":deployment_id}, start_time=start_time, end_time=end_time)
for metric in MetricsList(drift_data):
    if "mm_feature" in metric.label_config:
        feature = metric.label_config["mm_feature"]
        queries["drift"][feature] = f"mm_pval{{mm_id='{deployment_id}', mm_feature='{feature}'}}"

output = []

while start_time < end_time:
    
    dfs = []
    for metric,query in queries[args.type].items():
        data = prom.custom_query_range(
            query,
            start_time=start_time,
            end_time=start_time + timedelta(days=1),
            step=f"{args.s}m",
        )

        if len(data) == 0:
            continue
        
        data1 = [{"metric":x["metric"],"values":[ [float(value[0]),float(value[1])] for value in x["values"]]} for x in data]

        df=MetricRangeDataFrame(data1, columns=["timestamp","value"], dtype="Float64")
        #reinitialize df again from same values since df.describe somes failes on original df
        df = DataFrame(df.values, index=df.index, columns=df.columns, dtype="Float64")

        if df.empty:
            continue

        df=df.describe(percentiles=[]).rename(columns = {'value': metric })
        dfs.append(df)

    start_time += timedelta(days=1)
    if len(dfs) == 0:
        continue
    df = pd.concat(dfs, axis=1)
    df["date"] = start_time.date()
    output.append(df)
    
if len(output) == 0:
    print("No data found")
    sys.exit(0)
    
df = pd.concat(output)
df=df.set_index(['date'], append=True).reorder_levels(order = [1,0]).sort_index()

if args.output == sys.stdout:
    pd.options.display.width=None
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    print(df)
else:
    df.to_csv(args.output)