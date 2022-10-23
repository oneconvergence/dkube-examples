# MODEL MONITORING CHEST-XRAY EXAMPLE (UI)

## 1. Prerequisites
1. Make sure you created a dataset for storing labelled data
   - This is a remote dataset on Minio S3 cloudevents bucket.
2. Generate a Uniquer-ID as a path into Minio Cloudevents bucket for storing labels.
   - This could be your deployment UUID (preferred)
     - Click on Deployment Name. Deployment UUID is dispalyed on the top of the page
   - Or, this could be your user name.

## 2. Create Model Monitor
1. Click on Add Monitor in the Deployment's actions button.
2. In Basics Tab, select the following
  - Model type: Classification 
  - Input Data type: Image
  - Image Shape: Height:200, Width:200, Channels:1, Channel order: Channels Last
  - timezone: UTC.

### 2.2. Health Monitoring
1. Goto **Health** tab and Check Enable

### 2.3. Drift Monitoring
1. Check Enable and provide frequency as 5 minutes and algorithm as Kolmogorov-Smirnov.
2. **Add Train Data** : Configure the following
   - dataset: chest-xray
   - version: v1
   - Images saved as: Images in Labelled folder 
3. **Add Predict Data**: Configure the following
  - dataset content: CloudEventLogs.
     
### 2.4. Performance Monitoring
1. Check Enable
2. frequency: 5 minutes.
2. Compute Metrics: Labelled dataset
  -  Select dataset `chest-xray-labels`.
  -  Prefix/subpath: {Unique-ID}/livedata
  -  Dataset content : Tabular
  -  Files organized as: yyyy/dd/mm/hh
  -  Groundtruth column name: label
  -  Prediction column: output
  -  Timestamp column: timestamp
3. Click on Submit.

**Note:** Monitoring configuration is complete. Click Cancel on pop up and go back to the list of Monitors table.

## 3. Thresholds (Optional)
Add Soft & Hard thresholds for each metric
1. Download thresholds.json from code repo to your workstation
2. Click on *Upload Thresholds* icon under Actions against the monitor.
3. Upload the specified thresholds.json file
Note: You can update thresholds while monitor is running in Active state.

## 4. Alerts (Optional)
Add Performance Decay Alerts
1. Click on *Add Alerts* icon under Actions against the monitor.
2. Clock on *+ Add Alert* choose the following
  - Alert Name: accuracy
  - Alert Type: Performance Decay from dropdown.
  - Configure based on: Threshold
  - Configure condition - accuracy < 0.85
  - Submit

## 5. Start Monitor.
1. Goto Monitors table
2. Select the specific Monitor and Click on Start 
   - Modelmonitor can only be started in 'ready' state.
   - It can be stopped anytime. Previous data will not be erased.
