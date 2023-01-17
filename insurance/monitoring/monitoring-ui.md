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

 > **Note** The labels are generated in the example for purposes of illustration.  In an actual Production environment, the label data would be generated manually by experts in the domain.

 > **Note** You can choose the names for your resources in most cases.  It is recommended that you choose names that are unique to your workflow even if you are organizing them by Project.  This will ensure that there is a system-wide organization for the names, and that you can easily filter based on your own work.  A sensible approach might be to have it be something like **\<example-name\>-\<your-initials\>-\<resource-type\>**.  But this is simply a recommendation.  The specific names will be up to you.

## Set up Resources

### Create Code & Model Repos

 A deployed Model is used for this example, and the first step in this process is to create Code & Model repos.  This section explains how to accomplish this.

 > **Note** This step may have been completed in an earlier section of this example.  If so, skip the steps here and use the Code & Model repo names that you previously created.  If you need to create a new Code and/or Model repo, follow the instructions at:
 - [Create Code Repo](../readme.md#create-project)
 - [Create Model Repo](../readme.md#create-model-repo)

### Create & Launch JupyterLab IDE

 The Monitor setup is executed from a JupyterLab notebook.  This section explains how to create and launch the JupyterLab notebook.

 > **Note** This step may have been completed in an earlier section of this example.  If so, skip the steps here and use the JupyterLab IDE that you previously created.  If you need to create a new IDE, follow the instructions at:
 - [Create JupyterLab IDE](../readme.md#create-jupyterlab-ide) <br><br>
 - Once the IDE is in the "Running" state, select the JupyterLab icon on the far right of the IDE line
   - This will open a JupyterLab tab

## Train & Deploy Insurance Model

  In order to Monitor a Model in this example, it needs to be trained and deployed.  This section explains how to accomplish this.

 > **Note** This section requires a full DKube installation

 > **Note** This step may have been completed in an earlier section of the example.  If so, you can skip this section and use the deployed Model for the Monitor.  If you need to train and deploy the Model, follow the pipeline instructions at:
 - [Train and Deploy Model](../readme.md#create-kubeflow-pipeline)

  - The Pipeline will create a new Deployment.  It will be at the top of the Deployment list.
 
 > **Warning** Do not proceed until the Pipeline Run has completed and deployed the Model
 
### Execute File to Create Resources

 - Navigate to folder <code>/workspace/**\<your-code-repo\>**/insurance/monitoring</code>
 - Open `resources.ipynb` <br><br>
    > **Warning** Ensure that the last cell at the bottom of the file has `CLEANUP = False`  This may have been set to `True` from a previous execution.
   - Leave the other fields in their current selection
 - From the top menu item `Run`, Select `Run All Cells`
 - This will create the DKube resources required for this example to run the Monitor, including the required Datasets <br><br>
 - The following Datasets will be created:
   - `insurance-data`
     - This will have a pub_url source
     - This is the original training Dataset
   - `<your-performance-dataset>`
     - This Dataset includes the username and ends in "-s3"
     - This will have an "s3 | remote" source
     - This is the Dataset used for the Performance Monitoring <br><br>
   > **Note** Make note of the Dataset name *\<your-performance-dataset\>* for Performance Monitoring.  It will be used during the Monitor creation section.

### Review the Deployment & Identify the Deployment ID

 The Pipeline will create a new Deployment.  It will be at the top of the Deployment list.
 
 > **Note** The Deployment ID will be required during the Monitor Creation section.  The ID is available using the following steps:

 - Select the Deployment Name
 - The Deployment ID will is at the top of the screen.  It is of the form "dkube-insurance-pl-xxxxxx".
   - This will be used as **\<your-deployment-id\>** during the Monitor Creation section

## Create Monitor
 
 This section describes how to create a Monitor manually from a Deployed Model.
 
 > **Note** There are several fields which will be required during the Monitor creation process that are available from previous sections.  They need to be available prior to starting the Monitor creation process.
 
### Required Fields
 
 The following fields are required as part of the `Performance` tab in the Monitor creation process:
 
 - The name of the `Dataset` in the dropdown field comes from the `Resource.ipynb` script.  It is described in that section.
 - The name of the `Deployment ID` in the `Prefix/Subpath` field can be obtained as follows:
   - Navigate to the `Deployments` menu on the left
   - Select the Deployment name
   - The Deployment ID will is at the top of the screen.  It is of the form `dkube-insurance-pl-xxxxxx`.
 
### Monitor Creation Steps
 
 The Monitor is created from a Deployment in this example.  This section explains how to go through the process of entering the pertinent information into the fields for initial Monitor creation.  Follow-on section descibe how to complete the Monitor input.
 
 - Navigate to the `Deployments` menu on the left
 - Identify the Deployed Model that will be Monitored.  It will be the Model at the top of the list.
 - At the far right of that Model line, select `Add Monitor` icon
 - Fill in the required fields in the `Basic` tab as follows:
   - **Model Type:** `Regression`
   - **Input Data Type:** `Tabular`
   - Leave the other fields at their current selection <br><br>
 - Fill in the required fields in the `Drift` tab as follows:
   - Select `Enable` box
   - **Algorithm:** `Auto`
   - Within "Train Data" section use the following fields:
     - **Dataset:** `insurance-data`
     - **Dataset Version:** `v1`
     - Select the `Advanced` button
       - Upload Transformer Script file from [Transformer Script File](https://raw.githubusercontent.com/oneconvergence/dkube-examples/training/insurance/monitoring/mm-transformer.py)
   - Within the `Predict Data` section use the following fields:
     - **Dataset Content:** `CloudEventLogs`
   - Leave the other fields at their current selection <br><br>
 - Fill in the required field in the `Performance` tab as follows:
   - Select `Enable` box
   - Select `Labelled Data` box
   - **Dataset:** *`<your-performance-dataset>`* **(from Resource Creation step)**
   - **Prefix/Subpath:** <code>**\<your-deployment-id\>**/livedata</code> **(from Model Deployment section)**
   - **Groundtruth Column Name:** `GT_target`
   - **Prediction Column Name:** `charges`
   - **Timestamp Column Name:** `timestamp`
   - Select the `Advanced` box
     - **Dataset Content:** `Tabular`
   - Leave the other fields at their current selection
 - Select the `Submit` button
   - Choose `Close` from the popup
 
## Update Schema
 
 After the Monitor is initially created, you must configure the Schema to fully enable the Monitor.  The Schema characterizes the input and output features of the Model.  This section explains how to accomplish that.
 
 - Navigate to the `Deployments` menu on the left
 - Select the `Monitors` tab on the top
 - The newly created Monitor will show up on the list
   - The Monitor will be in the `pending` status.  If it is not yet at that status, wait until it is.
 - Select the `Update Schema` icon on the right of the Monitor line
   - The Schema window will appear
 - Change the following fields:
   - `charges` should be changed to `prediction output` through the `column/feature type` dropdown menu
   - `unique_id` should be selected as `RowID` and selected on the left box
   - `timestamp` should be selected as `Timestamp` and selected on the left box
   - Select the input features such as `age`, `sex`, `bmi`, and `region`
 - Select the `Save` button on the top right
 - Confirm that you want to save the changes
 - Choose `Go to Alerts` on the next popup

## Add Alerts
 
 Alerts are set to notify the user if a feature is not wihin the tolerance specified.  This section describes how to add alerts.  The Alerts screen will show up based on the previous selection.
 
 > **Note** The data generation script that will be run later in this example will create data that provides drift on the selected features
 
 > **Note** It is recommended that a separate alert be created for an individual feature for clarity
 
 ### Add Feature Drift Alert
 
  This will add an Alert for input Feature Drift.  The following threshold guidelines are recommended:
  - The thresholds must be between 0 and 1
  - Choose a threshold between 0.1 and 0.3 <Br><br>
 - Select the `+ Add Alert` button at the top right
 - Fill in the following fields as follows:
   - **Alert Name:** `age_alert`
   - **Alert Type:** `Data Drift`
   - **Configure based on:** `Threshold`
   - **Select Feature:** `age`
   - **Operator:** `>`  **(greater than)**
   - **Threshold:** `0.02`
 - Leave the other fields in their current selection
 - Select `Submit` button on the bottom right
 - This will show that the Alert has been set

### Add Performance Decay Alerts

 This will add an Alert for Performance decay.
                       
 - Select the `+ Add Alert` button
 - Fill in the following fields as follows:
   - **Alert Name:** `mae_alert`
   - **Alert Type:** `Performance Decay`
   - **Configure based on:** `Threshold`
   - **Select Metric:** `mae`
   - **Operator:** `>`  **(greater than)**
   - **Threshold:** `2000`
 - Leave the other fields in their current selection
 - Select `Submit` button on the bottom right
 - This will show that the Alert has been set
 
### Upload Threshold File
 
 It is possible to set a range of alert thresholds through a configuration file uploaded to DKube.  This section explains how to upload a threshold file.
 
 - Navigate to the `Deployments` menu on the left
 - Select the `Monitors` tab from the top
 - Select the `Upload Thresholds` icon on the far right of the Monitor line
 - Select the `Upload` button and use the Threshold file by right-clicking the link below, saving the address, and using that address in the popup window
   - [thresholds.json](https://raw.githubusercontent.com/oneconvergence/dkube-examples/training/insurance/monitoring/thresholds.json)
 
  > **Note** If you cannot directly paste in the link address, select the link by right-clicking it, select `Raw` on the right of the screen, save the file by right-clicking the screen and using `Save As...` to save the file.  Then use your new file to upload.
 
 > **Note** The Thresholds File does not set any alerts. It is only used for the visual indications (green, yellow, red) on the UI. One can set alerts later either based on these thresholds or completely new thresholds.

## Start Monitor
 
 After the Monitor has been set up, it is in the `Ready` state.  This means that the configuration has been complete, and the inputs are valid.  In order for the Monitor to operate, it needs to be running.  This section explains how to start the Monitor.
 
 - Navigate to the `Deployments` menu on the left
 - Select the `Monitors` tab from the top
 - The Monitor status will be `Ready`
   - If the Monitor is not in the `Ready` status, do not proceed.  It means that something is incomplete or in error.
 - Select the Monitor with the checkbox on the left
 - Select the `Start` button from the top
 - Confirm the start
 - Wait for the status to change to `active` before proceeding
 
 > **Note** The  Monitor can be stopped at any time by selecting it and using the `Stop` button on the top.  Previous data will not be erased when the Monitor is stopped.

## Generate Monitor Data

 In order for the Monitor to operate, predictions and groundtruth Datasets must be generated. 
 
 - From the JupyterLab tab, navigate to folder <code>/workspace/**\<your-code-repo\>**/insurance/monitoring</code>
 - Open `data_generation.ipynb`
 - In the 1st cell, specify the number of Dataset samples to run before stopping the data generation.  You can leave it at the default, or modify it.  The larger the number of samples, the more data will be generated for the Monitor graphs.
   - Leave the other fields at their current selection
 - `Run All Cells`
 - The script will start to push the data

## View the Monitor

 After the data has been generated for a few data points, it can be viewed within DKube.
 
 - Navigate to the `Deployments` menu on the left
 - Select the `Monitors` tab on the top
 - Your new Monitor will be at the top of the list
 - The details of how to view and understand the Monitor are described at [DKube Monitor Dashboard](https://dkube.io/monitor/monitor3_x/Monitor_Workflow.html#monitor-dashboard)
 > **Note** The graph may not show any data until the 2nd data generation push due to the timing of the monitoring
