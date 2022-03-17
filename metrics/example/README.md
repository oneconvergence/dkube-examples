This reference implementation is an example for a custom Performance Monitor exporting business metrics that are not directly supported by DKube.

### Custom Compute Metrics Usage for Modelmonitor
- Click on Deployments and navigate to the Monitors tab.
- Navigate to **Performance** tab for a model monitor and click on **Custom** under compute metrics.
- Give docker image as **ocdr/test-metrics:v2**
- Give Startup script as `python metrics.py
- Click on submit.

### Customize the script
- Reporting Performance Metrics
  - Update metric_name and metric_value
