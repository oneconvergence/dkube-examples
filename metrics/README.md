This folder contains examples for the following use cases

- [custom-metrics](custom-metrics) this contains an example for a custom Performance Monitor exporting business metrics that are not directly supported by DKube.
- [server](server) this containsan example for a custom deployment exporting health metrics
- [mm_metrics.py](mm_metrics.py) an utility to query prometheus and calculate statistics such as min/max/mean/std-deviation values for a metric. These are useful for deriving soft & hard thresholds

Computing metrics statistics
============================

1. pip3 install prometheus-api-client
2. Run following command to fetch metrics for a given deployment, metrics type and given duration (in days).

    a). To get deployment id, click on the deployment and copy the id
3. export DKUBE_URL and DKUBE_USER_ACCESS_TOKEN

    a) export DKUBE_URL="https://x.x.x.x:32222
    
    b) export DKUBE_USER_ACCESS_TOKEN="dkube oauth token"


$python3 ./mm_metrics.py -i 5a9af1a1-e3ca-4dbe-9546-783affad25d3 -n 4 -t health

```
                  requests_rate  4xx_requests_rate  5xx_requests_rate   latency  cpu_utilization  memory_utilization
date                                                                                                                
2022-02-27 50%            0.167                nan              0.000  4590.000            0.012       815390720.000
           count       1441.000              0.000           1441.000  1441.000         1441.000            1441.000
           max            0.433                nan              0.000  7519.125            0.030       815677440.000
           mean           0.201                nan              0.000  4648.848            0.015       815407166.534
           min            0.089                nan              0.000  2719.870            0.009       815239168.000
           std            0.078                nan              0.000   731.930            0.005          102375.402
2022-02-28 50%            0.244                nan              0.000  4562.077            0.020       815685632.000
           count       1441.000              0.000           1441.000  1441.000         1441.000            1441.000
           max            0.433                nan              0.000  7394.000            0.028       816095232.000
           mean           0.224                nan              0.000  4610.110            0.016       815726122.992
           min            0.089                nan              0.000  2785.619            0.006       815550464.000
           std            0.082                nan              0.000   670.256            0.005           99657.182
2022-03-01 50%            0.156                nan              0.000  4557.135            0.011       815874048.000
           count       1439.000              0.000            896.000  1328.000         1439.000            1439.000
           max            0.433                nan              0.000  7876.857            0.030       816787456.000
           mean           0.172                nan              0.000  4633.118            0.013       718440884.926
           min            0.000                nan              0.000  2353.792            0.000       600186880.000
           std            0.085                nan              0.000   789.397            0.005       107644439.985
2022-03-02 50%            0.167                nan              0.000  4591.286            0.013       848949248.000
           count       1441.000              0.000           1441.000  1166.000         1441.000            1441.000
           max            0.433                nan              0.000 30064.500            0.032       878534656.000
           mean           0.182                nan              0.000  4626.437            0.017       813822742.207
           min            0.000                nan              0.000     4.582            0.004       600207360.000
           std            0.114                nan              0.000  1112.746            0.006       104655353.194
```
