Metric Server is a service which allows exporting metrics from cluster not directly supported by DKube. 

A reference implementation is provided here. At the minimum metric server needs to implement query_range api and return the response in expected format.


Running Metric Server
=====================

1. pip install poetry
2. poetry install
3. uvicorn server.main:app 
4. goto http://127.0.0.1:8000/docs
5. Authorize with any username/password
6. Try out query_range api with sample inputs

Supported Metrics
=================
Following metrics are supported.

| Metric      | Description |
| ----------- | ----------- |
| Invocations | The number of total prediction requests sent to a model endpoint.|
| Invocation4XXErrors | The number of prediction requests where the model returned a 4xx HTTP response code.|
| Invocation5XXErrors | The number of prediction requests where the model returned a 5xx HTTP response code.|
| ModelLatency | Sum of Time taken to process the prediction requests. In microseconds.|
| CPUUtilization | The sum of each individual CPU core's utilization. The CPU utilization of each core range is 0–100. For example, if there are four CPUs, the CPUUtilization range is 0%–400%.|
| MemoryUtilization | Amount of memory used by the prediction process. In bytes.|