# Model Monitoring Insurance Example

#### Note : For model training/retraining with DKube, follow the README https://github.com/oneconvergence/dkube-examples/tree/sklearn/insurance

## Add Training-Data in Dkube
1. Provide name eg: “s3-insurance-traindata”
2. Versioning: None
3. Source s3:
4. Check for AWS
5. Provide your aws key and secret
6. Bucket: mm-workflow
7. Prefix: insurance-base
8. Save

## CREATE MODEL MONITOR

1. From model monitoring create a new monitor
2. Give a name.
3. Add tag d3qatest
4. select the added model.
5. Select Model Type: Regression
6. Change model run frequency to 5 hours. (in UI it’s five hours but it will run in every 5 mins because of d3qatest tag)
7. Submit

## Add training data (s3-insurance-traindata)
1. Prefix: insurance-datasets/training-data/
2. Type: CSV
3. Add transformer script: https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/transformer.py
4. Note: Download the script in your setup and then add it by browsing.
5. Save training data.

## Update Schema
1. Edit the model monitor
2. Go to schema and change
3. charges as prediction output - continuous
4. unique_id as RowID - continuous
5. Timestamp as timestamp - continuous
6. Change value type: Age and bmi to continuous
7. Select all Input features and unselect charges, unique_id, and timestamp.
8. Click Next and save.

## Data Generation
1. Run data_generation.ipynb notebook for generating predict and groundtruth datasets.
2. In 1st Cell Fill MonitorName with the name of your monitor name MonitorName="{your_model_monitor_name}"
3. In 1st cell, Update Frequency according to what you set in Modelmonitor. If the d3qatest tag was provided replace it with to use frequency in minutes. For eg: for 5 minutes replace it with `5m` else use `5h` for hours assuming Frequency specified in monitor was 5.
4. Then Run All Cells. It will start Pushing the data.
5. After First Push of dataset by this script. Configure the generated datasets in modelmonitor.

## Configure Following Dataset in modelmonitor
-  **Predict Dataset**
-  Dataset: {model-monitor}-predict
-  Type: CSV

- **Labelled Dataset**
- Dataset: {model-monitor}-groundtruth
- Type: CSV

- **Ground Truth Column Name**: GT_target
- **Prediction Column Name**: charges

6. After that add Alerts - generally this script will be creating alert on features age, sex, bmi, region. Configure one alert for each individual feature. With threshold between 0 to 1. generally advised 0.02 to 0.03 inclusive.
7. Start Monitor.

