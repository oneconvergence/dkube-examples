# MODEL MONITORING INSURANCE EXAMPLE (UI)


## 1. Create Model Monitor
1. Deployment in Dkube can be external or local, if it is local then move to step2 directly. 
- If it is external, click on Deployments in the left tab and import a deployment by filling the details. 
  - For this example, you could import a Deployment just by specifying the same name you specified in resources.ipynb for MONITOR_NAME and click on Import and submit the form. None of the other parameters need to be filled in.
2. click on Add Monitor in the actions tab.
3. In Basics Tab, select the **Model type** as Regression, **Model input** as Tabular and give the timezone as UTC.

### 2. Drift Monitoring
1. Goto Drift tab
2. Check Enabled option and provide frequency as 5 minutes and algorithm as auto.
3. **Add Train Data** :
-  If data source is **aws_s3 / local**
   - Select dataset as insurance-data and version as v1 if your data source is aws_s3 or local.
   - Upload transformer script from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/insurance_datasources/transform-data.py)
- If your datasource is **sql**
  - Select dataset as insurance-data-sql.
  - Select dataset format as Tabular.
  - Provide sql query as "select * from insurance"
  - Upload transformer script from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/insurance_datasources/transform-data.py)

3. **Add Predict Data**:
- If data source is **aws_s3 / local**
     -  Select dataset as {MONITOR_NAME}-predict.
     -  If the dataset is local then select the version as v1.
     -  Select dataset format as Tabular.
     -  Date suffix is yyyy/dd/mm/hh
- If your datasource is **sql**, 
    - Select dataset as insurance-data-sql.
    - Select dataset format as Tabular.
    - Provide sql query as "select * from insurance_predict"

### 4. Performance Monitoring
1. Goto Performance tab
2. Check Enabled option and provide frequency as 5 minutes 
2. In Compute Metrics select Labelled dataset
1. **If source is S3** :
  -  Dataset: {model-monitor}-groundtruth
  -  Dataset Format : Tabular
  -  Select Prediction column name as “charges”
  -  Select Groundtruth column name as GT_target.

2. **If source is local** :
  -  Dataset: {model-monitor}-groundtruth
  -  Dataset Format : Tabular
  -  Select Dataset Version as v1.
  -  Select Prediction column name as “charges”
  -  Select Groundtruth column name as GT_target.

3. **If source is sql**:
- Dataset : insurance-data-sql
- Sql query field : select * from insurance_gt
- Dataset Format : Tabular
- Select Prediction column name as “charges”
- Select Groundtruth column name as GT_target.

4. Click on Submit. 
- Monitor goes to baselining state while it performs transformation and computes schema.
- When the computation completes, it automatically takes you to schema page.
- You could also choose go back to Dashboard and click on update schema action.

### 5. Update Schema
1. If you are already on schema page, go to step 2. Otherwise, click on update schema action button.
2. Update the following
  - charges as prediction output.
  - unique_id as RowID
  - Timestamp as timestamp
  - Select all or interested Input features.
4. Click Next and save.

### 6. Alerts
Add Feature Drift Alerts
 - The datageneration script will be generating drift on the following features - age, sex, bmi, region.
 - Suggest to configure a separate alert for each individual feature.
 - Use a threshold between 0 to 1. generally advised 0.01 to 0.1 for all categorical or all continuous columns columns.
 - It fires an alert when calculated drift goes under the configured threshold.

Add Performance Decay Alerts
  - Create an alert and choose Performance Decay from dropdown.
  - Select absolute and choose metrics from down.
  - Provide absolute threshold value. 
    - Example. for mae metric, specify 2000 as threshold
    - Depending on the metric, choose > or < operator. For mae, choose >
  - It fires an alert when mae value goes above 2000

Notes:
 - You could also configure *Breach incidents*. If the metric continuously braches the specified number of times, it is considered alert. 
 - A follow up action could be specified to send an email. SMTP configuration needs to be specified on Configuration page on Operator view.
 - You could also combine multiple conditions while creating an alert. This can be done by clicking on *+* button
A complex 

### 7. Thresholds
1. Click on *Upload thresholds* and upload the sample thresholds from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/insurance_datasources/thresholds.json)
- Soft and Hard thresholds are configured for each metric. Status of a metric is computed as follows.
  - Breaching soft threshold is considered a warning and is represented using the color *Orange*
  - Breaching hard threshold is considered critical and is represented using the color *Red*
  - Otherwise the metric is considered healthy and is represented using the color *Green*
- This computed information is also shown on monitors tab. 
  - Drift monitoring is considered critical if any one of the drift features are in critical state
  - Performance monitoring is considered critical if any one of the performance metrics are in critical state

### 7. Start Monitor.
Click on Start for the specific monitor on Modelmonitor dashboard.
   - Modelmonitor can only be started in 'ready' state.
   - It can be stopped anytime. Previous data will not be erased.

