# Model Monitoring Insurance Example

## INSURANCE MODEL CREATION :

### Code

1. Add Code **insurance**
  - Source: Git
  - URL: https://github.com/oneconvergence/dkube-examples.git
  - Branch : monitoring

### Dataset (AWS OR SQL)

- Note: Skip this step if your data is in aws-s3.It will be automatically created in pipeline.

1. Add dataset **insurance-data**
2. Versioning: None
3. Source : SQL
4. Provider : MYSQL
5. Select password and fill the details
   - Username : **
   - Password : **
   - HostAddress: **
   - PortNumber : **
   - Database Name : monitoring

### Pipeline

1. From **workspace/insurance/insurance** run **pipeline.ipynb** to build the pipeline.In 1st cell, for retraining specify input_train_type = 'retraining' and specify the source if your data is in sql.
2. The pipeline includes preprocessing, training and serving stages. 
  - **preprocessing**: the preprocessing stage generates the dataset (either training-data or retraining-data) depending on user choice.
  - **training**: the training stage takes the generated dataset as input, train a sgd model and outputs the model.
  - **serving**: The serving stage takes the generated model and serve it with a predict endpoint for inference. 


### Inference
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command  
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance 
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.


## MODEL MONITOR

1. From model monitoring create a new monitor
2. Give a name.
3. Add tag d3qatest
4. select the added model.
5. Select Model Type: Regression
6. Change model run frequency to 5 hours. (in UI it’s five hours but it will run in every 5 mins because of d3qatest tag)
7. Submit

## Add training data 
1. Prefix: mm-demo/training-data
2. Type: CSV
3. Add transformer script: https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/transform-data.py
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
2. In 6th Cell Fill MonitorName with the name of your monitor name MonitorName="{your_model_monitor_name}"
3. In 6th cell, Update Frequency according to what you set in Modelmonitor. If the d3qatest tag was provided replace it with to use frequency in minutes. For eg: for 5 minutes replace it with `5m` else use `5h` for hours assuming Frequency specified in monitor was 5.
4. In 6th cell. Set DATASET_SOURCE as DataSource.SQL if you want to push the data in SQL and fill the below details hostname,username,password,database_name.
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

