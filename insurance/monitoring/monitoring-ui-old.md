# MODEL MONITORING INSURANCE CLOUDEVENTS EXAMPLE (UI)

## 1. Create Model Monitor
1. Deployment in Dkube can be external or local, if it is local then move to step2 directly. 
If it is external, then first add the cluster and click on Deployments in the left tab and import a deployment by filling the details.
2. Make Sure the Deployment is in running state. 
3. Run the `resources.ipynb` to create the required resources.
4. Copy the deployment-id from deployment details page and keep it with you.
5. click on Add Monitor in the actions tab.
6. In Basics Tab, select the Model type as Regression, Input data type Tabular and timezone as UTC.

### 2. Drift Monitoring
1. Check Enable and provide frequency as 5 minutes and algorithm as auto.
2. **Add Train Data** :
   - Select dataset as `insurance-data` and version as v1 if your data source is aws_s3 or local.
   - Upload transformer script from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/training/insurance/monitoring/mm-transformer.py)

3. **Add Predict Data**:
 -  Select dataset content as **Cloudevents**.

### 3. Performance Monitoring
1. Check Enable and provide frequency as 5 minutes.
2. In Compute Metrics select Labelled dataset
  -  Select dataset `insurance-mm-kf-s3`.
  -  Prefix/subpath: {deployment ID}/livedata
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
 - Use a threshold between 0 to 1. generally advised 0.1 to 0.3 for all categorical or all continuous columns columns,  0.1 to 0.3 for mixed categorical and continuous columns columns.
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

### 8. Data Generation
 - Go to the IDE and open `workspace/insurance/insurance/monitoring/data_generation.ipynb`
 - Run all cells.
