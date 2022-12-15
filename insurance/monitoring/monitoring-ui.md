# Create Monitor for Insurance Prediction Example Through UI

 This section explains how to create a Monitor for the insurance prediction example using the DKube UI.

 - This example uses the DKube built-in MinIO server and uses prediction datasets as "CloudEvents"
 - This example assumes that the serving cluster and the model monitoring cluster are the same

## Example Flow
 - Create the DKube resources
 - Train a model for the Insurance example using TensorFlow and deploy the model for inference
 - Create a Model Monitor
   - Although a deployed Model is not required for a Monitor within DKube, this example uses a deployed model
 - Generate data for analysis by the Monitor
   - Predict data: Inference inputs/outputs
   - Label data:  Dataset with Groundtruth values for the inferences made above
 - Cleanup the resources after the example is complete

 > **_Note:_** The labels are generated in the example for purposes of illustration.  In an actual Production environment, the label data would be generated manually by experts in the domain.

## Set up Resources

### Create Code & Model Repos

 > **_Note:_** This step may have been completed in an earlier section of this example.  If so, skip the steps here and use the Code & Model repo names that you previously created.  If you need to create a new Code and/or Model repo, follow the instructions at:
 - [Create Code Repo](../readme.md#create-project)
 - [Create Model Repo](../readme.md#create-model-repo)

### Create & Launch JupyterLab IDE

 > **_Note:_** This step may have been completed in an earlier section of this example.  If so, skip the steps here and use the JupyterLab IDE that you previously created.  If you need to create a new IDE, follow the instructions at:
 - [Create JupyterLab IDE](../readme.md#create-jupyterlab-ide) <br><br>
 - Once the IDE is in the "Running" state, select the JupyterLab icon on the far right of the IDE line
   - This will create a JupyterLab tab

### Execute File to Create Resources

 - Navigate to "/workspace/\<your-code-repo\>/insurance/monitoring"
 - Open "resources.ipynb"
 - In the 1st cell, Fill in the external IP address for the field "SERVING_DKUBE_URL" in the form "https://\<External IP Address\>:32222/"
   - Ensure that there is a final "/" in the url field
   - Leave the other fields in their current selection
 - From the top menu item "Run", Select "Run All Cells"
 - This will create the DKube resources required for this example to run the Monitor, including the required Datasets <br><br>
 - The following Datasets will be created
   - "insurance-data", with a pub_url source
   - A Dataset that includes the username and ends in "-s3", with an "s3 | remote" source

## Train & Deploy Insurance Model
 
 In order to Monitor a Model in this example, it needs to be trained and deployed.
 > **_Note:_** This section requires DKube Runs, Kubeflow Pipelines, and KServe.  It requires a full DKube installation.

 > **_Note:_** This step may have been completed in an earlier section of the example.  If so, you can skip this section and use the deployed Model for the Monitor.  If you need to train and deploy the Model, follow the pipeline instructions at:
 - [Train and Deploy Model](../readme.md#create-kubeflow-pipeline)

 - The Pipeline will create a new Deployment.  It will be at the top of the Deployment list.


<!--- We are only describing a local deployment here, similar to the automatic generation
## 1. Create Model Monitor
1. Deployment in Dkube can be external or local, if it is local then move to step2 directly. 
If it is external, then first add the cluster and click on Deployments in the left tab and import a deployment by filling the details.
2. Make Sure the Deployment is in running state. 
3. Run the `resources.ipynb` to create the required resources.
4. Copy the deployment-id from deployment details page and keep it with you.
5. click on Add Monitor in the actions tab.
6. In Basics Tab, select the Model type as Regression, Input data type Tabular and timezone as UTC.
--->

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
