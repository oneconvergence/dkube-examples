# MODEL MONITORING INSURANCE SAGEMAKER EXAMPLE (UI)


## 1. Create Model Monitor
1. Deployment in Dkube need to be external. First add the sagemaker cluster, and click on Deployments in the left tab and import a deployment by filling the details.
2. click on Add Monitor in the actions tab.
3. In Basics Tab, select the Model type as Regression and give the timezone as UTC.

## 2. Add resources:
1. **Add Cluster**
  - From operator page add cluster.
  - Cluster type Sagemaker
  - Select Access keys authentication method.
  - Provide your AWS access keys and region.
  - Click Add cluster.
2. **Add predict dataset**
  - Dataset Nmae: {MONITOR_NAME}-predict
  - Versioning: None
  - Source: S3
  - Provide your AWS credentials
  - Bucket: Sagemaker log bucket
  - Prefix: sagemaker/Demo-ModelMonitor/datacapture/{MONITOR_NAME}/AllTraffic/

### 2. Drift Monitoring
1. Check Enable and provide frequency as 5 minutes and algorithm as auto.
2. **Add Train Data** :
   - Select dataset as `insurance-data` and version as v1 if your data source is aws_s3 or local.
   - Upload transformer script from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/insurance/transform-data.py)

3. **Add Predict Data**:
- If data source is **aws_s3 / local**
     -  Select dataset {MONITOR_NAME}-predict.
     -  Select dataset content as **Sagemakerlogs**.
     -  Date suffix is yyyy/dd/mm/hh

### 3. Performance Monitoring
1. Check Enable and provide frequency as 5 minutes.
2. In Compute Metrics select Labelled dataset
  -  Select dataset {MONITOR_NAME}-groundtruth.
  -  Dataset Format : Tabular
  -  Fill Prediction column name as “charges”
  -  Fill Groundtruth column name as "GT_target".
  -  Fill timestamp column as "timestamp"

3. Click on Submit.

### 4. Update Schema
1. Edit the model monitor
2. Go to schema and change
  - charges as prediction output.
  - unique_id as RowID
  - Timestamp as timestamp
3. Select all or interested Input features.
4. Click Next and save.

### 5. Alerts
Add Feature Drift Alerts
 - The datageneration script will be generating drift on the following features - age, sex, bmi, region.
 - Suggest to configure a separate alert for each individual feature.
 - Use a threshold between 0 to 1. generally advised 0.05 to 0.1 for all categorical or all continuous columns columns,  0.05 to 0.01 for mixed categorical and continuous columns columns.
 - It fires an alert when calculated drift goes under the configured threshold

Add Performance Decay Alerts
  - Create an alert and choose Performance Decay from dropdown.
  - Select `mse` metric from down.
  - Provide 2000 as threshold value.

### 6. Upload threshold file, 
- From model monitor actions, click on Upload thresholds. 
- Download the threshold file [thresholds.json](https://github.com/oneconvergence/dkube-examples/blob/monitoring/insurance_cloudevents/thresholds.json) and upload.

### 7. Start Monitor.
Click on Start for the specific monitor on Modelmonitor dashboard.
   - Modelmonitor can only be started in 'ready' state.
   - It can be stopped anytime. Previous data will not be erased.