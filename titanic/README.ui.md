# MODEL MONITORING TITANIC CLASSIFICATION EXAMPLE (UI)

## 1. Create Model Monitor
1. From model monitoring create a new monitor
2. Give a name.
3. Add tag d3qatest
4. select the added model.
5. Select Model Type: Classification
6. Change model run frequency to 5 hours. (in UI it’s five hours but it will run in every 5 mins because of d3qatest tag)
7. Submit

### 2. Add training data 
1. Name : titanic-data 
   - This is DKube local dataset, created by the train.ipynb pipeline above

2. If training data source is S3/d3 select version: eg. v1
   - Type : csv
3. If training data source is SQL
      - Name: titanic-data-sql
      - Add query: `select * from titanic` (the table name can be different)
      - Save training data.
4. Download the [transformer script](https://github.com/oneconvergence/dkube-examples/tree/monitoring/titanic/transform_data.py) for s3/d3 data source and upload. 
5. Note: Download the script in your setup and then add it by browsing and save training data.


### 3. Update Schema
1. Edit the model monitor
2. Go to schema and change
  - Survived as prediction output.
  - PassengerId as RowID
  - Timestamp as timestamp
3. Select all or interested Input features.
4. Click Next and save.

### 4. Configure Following Dataset in modelmonitor
**Predict Dataset**
1. If source S3 or local
  -  Dataset: {model-monitor}-predict
  -  Type: CSV
2. If source SQL
      - Dataset: titanic-data-sql
      - Query: `select * from titanic_predict` (table will be added to the DB by the datagen script)

**Labelled Dataset**
1. If source S3 or local
  -  Dataset: {model-monitor}-groundtruth
  -  Type: CSV
2. If source SQL
      - Dataset: titanic-data-sql
      - Query: `select * from titanic_gt` (table will be added to the DB by the datagen script)

- **Ground Truth Column Name**: GT_target
- **Prediction Column Name**: Survived

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
