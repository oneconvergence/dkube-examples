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

 - Navigate to "/workspace/*\<your-code-repo\>*/insurance/monitoring"
 - Open "resources.ipynb"
 - In the 1st cell, Fill in the external IP address for the field "SERVING_DKUBE_URL" in the form "https://\<External IP Address\>:32222/"
   - Ensure that there is a final "/" in the url field
   - Leave the other fields in their current selection
 - From the top menu item "Run", Select "Run All Cells"
 - This will create the DKube resources required for this example to run the Monitor, including the required Datasets <br><br>
 - The following Datasets will be created:
   - "insurance-data"
     - This will have a pub_url source
     - This is the original training Dataset
   - *\<your-performance-dataset\>*
     - This Dataset includes the username and ends in "-s3"
     - This will have an "s3 | remote" source
     - This is the Dataset used for the Performance Monitoring <br><br>
   > **_Note:_** Make note of the Dataset name *\<your-performance-dataset\>* for Performance Monitoring.  It will be used during the Monitor creation section.

## Train & Deploy Insurance Model
 
 In order to Monitor a Model in this example, it needs to be trained and deployed.
 > **_Note:_** This section requires DKube Runs, Kubeflow Pipelines, and KServe.  It requires a full DKube installation.

 > **_Note:_** This step may have been completed in an earlier section of the example.  If so, you can skip this section and use the deployed Model for the Monitor.  If you need to train and deploy the Model, follow the pipeline instructions at:
 - [Train and Deploy Model](../readme.md#create-kubeflow-pipeline)

### Review the Deployment & Identify the Deployment ID

 The Pipeline will create a new Deployment.  It will be at the top of the Deployment list.
 
 > **_Note:_** The Deployment ID will be required during the Monitor Creation section.  The ID is available using the following steps:

 - Select the Deployment Name
 - The Deployment ID will is at the top of the screen.  It is of the form "dkube-insurance-pl-xxxxxx".  This will be used as *\<your-deployment-id\>* during the Monitor Creation section.

## Create Monitor
 
 This section describes how to create a Monitor manually from a Deployed Model.
 
 - Navigate to "Deployments" menu on the left
 - Identify the Deployed Model that will be Monitored.  It will be the Model at the top of the list.
 - At the far right of that Model line, select "Add Monitor"
 - Fill in the required fields in the "Basic" tab as follows:
   - Model Type: `Regression`
   - Input Data Type: `Tabular`
   - Leave the other fields at their current selection <br><br>
 - Fill in the required fields in the "Drift" tab as follows:
   - Select `Enable` box
   - Algorithm: `Auto`
   - Within "Train Data" section use the following fields:
     - Dataset: `insurance-data`
     - Dataset Version: `v1`
     - Upload Transformer Script file from [Transformer Script File](https://raw.githubusercontent.com/oneconvergence/dkube-examples/training/insurance/monitoring/mm-transformer.py)
   - Within the "Predict Data" section use the following fields:
     - Dataset Content: `CloudEventLogs`
   - Leave the other fields at their current selection <br><br>
 - Fill in the required field in the "Performance" tab as follows:
   - Select `Enable` box
   - Select `Labelled Data` box
   - Dataset: *`<your-performance-dataset>`* **(from Resource Creation step)**
   - Prefix/Subpath: *`<your-deployment-id>/livedata`* **(from Model Deployment section)**
   - Dataset Content: `Tabular`
   - Prediction Column Name: `charges`
   - Groundtruth Column Name: `GT_target`
   - Timestamp Column Name: `timestamp`
 - Leave the other fields at their current selection
 - Select the "Submit" button

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
