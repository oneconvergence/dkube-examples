# MODEL MONITORING IMAGE EXAMPLE (UI)

## 1. Create Model Monitor
1. Deployment in Dkube can be external or local, if it is local then move to step2 directly. 
If it is external, then first add the cluster and click on Deployments in the left tab and import a deployment by filling the details.
2. click on Add Monitor in the actions tab.
3. In Basics Tab, select the Model type as Classification and add below details, 
  - Data type: Image
  - Image Shape: Height:200, Width:200, Channels:1, Channel order: Channels Last
  - timezone as UTC.

### 2. Drift Monitoring
1. Check Enable and provide frequency as 5 minutes and algorithm as Kolmogorov-Smirnov.
2. **Add Train Data** :
   - Select dataset as `chest-xray` and version as v1 if your data source is aws_s3 or local.

3. **Add Predict Data**:
- Select dataset content as **Cloudevents**.
     

### 3. Performance Monitoring
1. Check Enable and provide frequency as 5 minutes.
2. In Compute Metrics select Labelled dataset
  -  Select dataset `image-mm-kf-s3`.
  -  Prefix/subpath: {deployment ID}/livedata
  -  Dataset Format : Tabular
  -  Date suffix is yyyy/dd/mm/hh
  -  Fill Prediction column name as output
  -  Fill Groundtruth column name as "label".
  -  Fill timestamp column as "timestamp"

3. Click on Submit.

### 5. Alerts
Add Performance Decay Alerts
  - Create an alert and choose Performance Decay from dropdown.
  - Select `accuracy` metric from down.
  - Provide 0.85 as threshold value.

### 6. Start Monitor.
Click on Start for the specific monitor on Modelmonitor dashboard.
   - Modelmonitor can only be started in 'ready' state.
   - It can be stopped anytime. Previous data will not be erased.
