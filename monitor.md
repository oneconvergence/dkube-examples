# MODEL MONITORING CHEST-XRAY EXAMPLE (UI)

## 1. Prerequisites
1. Make sure you created a dataset for storing labelled data
   - This is a remote dataset on Minio S3 cloudevents bucket.
2. Generate a Uniquer-ID as a path into Minio Cloudevents bucket for storing labels.
   - This could be your deployment UUID 
     - Click on Deployment Name. Deployment UUID is dispalyed on the top of the page
   - Or, this could be your user name.

## 2. Create Model Monitor
1. Click on Add Monitor in the Deployment's actions button.
2. In Basics Tab, select the Model type as Classification and add below details, 
  - Data type: Image
  - Image Shape: Height:200, Width:200, Channels:1, Channel order: Channels Last
  - timezone as UTC.

### 2.2. Health Monitoring
1. Goto **Health** tab and Check Enable

### 2.3. Drift Monitoring
1. Check Enable and provide frequency as 5 minutes and algorithm as Kolmogorov-Smirnov.
2. **Add Train Data** :
   - Select dataset as `chest-xray` and version as v1.
   - Select *Images in Labelled folder* for *Images saved as* field 
3. **Add Predict Data**:
- Select dataset content as *CloudEventLogs*.
     
### 2.4. Performance Monitoring
1. Check Enable and provide frequency as 5 minutes.
2. In Compute Metrics select Labelled dataset
  -  Select dataset `image-mm-kf-s3`.
  -  Prefix/subpath: {Unique-ID}/livedata
  -  Dataset Format : Tabular
  -  Date suffix is yyyy/dd/mm/hh
  -  Fill Prediction column name as output
  -  Fill Groundtruth column name as "label".
  -  Fill timestamp column as "timestamp"
3. Click on Submit.

**Note:** Monitoring configuration is complete. You will now go back to the list of Monitors table.

## 3. Thresholds (Optional)
Add Soft & Hard thresholds for each metric
1. Click on *Upload Thresholds* icon under Actions against the monitor.
2. Upload the specified thresholds.json file
Note: You can update thresholds while monitor is running in Active state.

## 4. Alerts (Optional)
Add Performance Decay Alerts
1. Click on *Add Alerts* icon under Actions against the monitor.
2. Clock on *+ Add Alert* choose Performance Decay from dropdown.
  - Select `accuracy` metric from down.
  - Provide 0.85 as threshold value.

## 5. Start Monitor.
1. Select the specific Monitor and Click on Start 
   - Modelmonitor can only be started in 'ready' state.
   - It can be stopped anytime. Previous data will not be erased.
