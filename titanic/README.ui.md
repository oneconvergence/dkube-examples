# MODEL MONITORING INSURANCE EXAMPLE (UI)


## 1. Create Model Monitor
1. Deployment in Dkube can be external or local, if it is local then move to step2 directly. 
If it is external, click on Deployments in the left tab and import a deployment by filling the details.
2. click on Add Monitor in the actions tab.
3. In Basics Tab, select the Model type as Classification and give the timezone as UTC.

### 2. Drift Monitoring
1. Check Enabled option and provide frequency as 5 minutes and algorithm as auto.
2. **Add Train Data** :
-  If data source is **aws_s3 / local**
   - Select dataset as titanic-data and version as v1 if your data source is aws_s3 or local.
   - Upload transformer script from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/titanic/transform-data.py)
- If your datasource is **sql**
  - Select dataset as titanic-data-sql
  - Select dataset format as Tabular.
  - Provide sql query as "select * from titanic"
  - Upload transformer script from [link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/titanic/transform-data.py)

3. **Add Predict Data**:
- If data source is **aws_s3 / local**
     -  Select dataset as {MONITOR_NAME}-predict.
     -  If the dataset is local then select the version as v1.
     -  Select dataset format as Tabular.
     -  Date suffix is yyyy/dd/mm/hh
- If your datasource is **sql**, 
    - Select dataset as titanic-data-sql.
    - Select dataset format as Tabular.
    - Provide sql query as "select * from titanic_predict"

### 3. Update Schema
1. Edit the model monitor
2. Go to schema and change
  - Survived as prediction output.
  - PassengerId as RowID
  - Timestamp as timestamp

3. Select all or interested Input features.
4. Click Next and save.

### 4. Performance Monitoring
1. Check Enabled option and provide frequency as 5 minutes and upload soft thresholds from [link]([link](https://raw.githubusercontent.com/oneconvergence/dkube-examples/monitoring/insurance/performance_soft_thresholds.json)
)
2. In Compute Metrics select Labelled dataset
1. **If source is S3** :
  -  Dataset: {model-monitor}-groundtruth
  -  Dataset Format : Tabular
  -  Select Prediction column name as “Survived”
  -  Select Groundtruth column name as GT_target.

2. **If source is local** :
  -  Dataset: {model-monitor}-groundtruth
  -  Dataset Format : Tabular
  -  Select Dataset Version as v1.
  -  Select Prediction column name as “Survived”
  -  Select Groundtruth column name as GT_target.

3. **If source is sql**:
- Dataset : insurance-data-sql
- Sql query field : select * from titanic_gt
- Dataset Format : Tabular
- Select Prediction column name as “Survived”
- Select Groundtruth column name as GT_target.

4. Click on Submit.

### 5. Alerts
Add Feature Drift Alerts 
 - The datageneration script will be generating drift on the following features - age, fare, Pclass, Sibsp, Sex
 - Suggest to configure a separate alert for each individual feature. 
 - Use a threshold between 0 to 1. generally advised 0.05 to 0.1 for all categorical or all continious columns columns,  0.05 to 0.01 for mixed categorical and continious columns columns.
 - It fires an alert when calculated drift goes under the configured threshold

Add Performance Decay Alerts
  - Create an alert and choose Perormance Decay from dropdown.
  - Selct percentage and choose metrics from down.
  - Provide percentage threshold value betweeen 5 to 10 and save.

### 6. Start Monitor.
Click on Start for the specific monitor on Modelmonitor dashboard. 
   - Modelmonitor can only be started in 'ready' state.
   - It can be stopped anytime. Previous data will not be erased.

