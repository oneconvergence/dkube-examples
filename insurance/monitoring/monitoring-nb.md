# Create Monitor for Insurance Prediction Example Automatically

 This section explains how to use a JupyterLab `.ipynb` file to create a Monitor for the insurance prediction example.

 - This example uses the DKube built-in MinIO server and uses prediction datasets as "CloudEvents"
 - The serving cluster can be the same as the monitoring cluster, or a separate monitoring cluster can be used, as described below

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

 This example uses a script to create the monitor resources necessary for the monitor creation.  This section explains how to run the script.
 
 - From the JupyterLab tab, navigate to folder <code>/workspace/**\<your-code-repo\>**/insurance/monitoring</code>
 - Open `resources.ipynb` <br><br>
   > **Warning** Ensure that the last cell at the bottom of the file has `CLEANUP = False`  This may have been set to `True` from a previous execution.
 - If the serving and monitoring cluster **are the same**, the script will get all of the fields automatically.
   - Ensure that the variable `SERVING_CLUSTER_EXECUTION` in the 1st cell is set to `True`
   - Leave the other fields in their current selection
   - Skip to the section "Run the Script"
 - If the serving cluster is **different from** the monitoring cluster, the serving cluster needs to be identified
   - In the 3rd cell, identified as `User Definitions, set `SERVING_CLUSTER_EXECUTION = False`
   - Complete the following fields in the 1st cell
     - `SERVING_DKUBE_URL` = External IP address for the **serving** cluster in the form:
       - "<code>https://**\<External IP Address\>**:32222/</code>"
       - Ensure that there is a final `/` in the url field
     - `MONITORING_DKUBE_URL` = "URL of the Monitoring cluster"
     - `MONITORING_DKUBE_USERNAME` = "Username on the Monitoring cluster"
     - `MONITORING_DKUBE_TOKEN` = "Access token for the Monitoring cluster, available from the `Developer Settings` menu at the top right of the screen <br><br>
     - If the Monitoring cluster already has a link to the Serving cluster from the DKube Clusters Operator screen:
       - Get the name of the DKube cluster link and provide that name to the variable `SERVING_DKUBE_CLUSTER_NAME`
     - If the Monitoring cluster link has **not** been created by the Operator on the Monitoring cluster:
       - Leave the variable `SERVING_DKUBE_CLUSTER_NAME = ""`
       - In that case, the link will be created on the Monitoring cluster
       - The username identified in the `MONITORING_DKUBE_USERNAME` variable must have Operator privileges for this to work.  If not, the script fill fail.
   - Leave the other fields in their current selection
 #### Run the Script
 - From the top menu item `Run`, select `Run All Cells`
 - This will create the DKube resources required for this example to run automatically, including the required Datasets <br><br>
 - The following Datasets will be created
   - `insurance-data`, with a pub_url source
   - A Dataset that includes the deployment name with "-s3" at the end, with an "s3 | remote" source

## Create Monitor Automatically

 In this example, the Monitor is created programmatically through the DKube SDK. 
 
 > **Warning** The script in this section will fail if there is already a Monitor with the automatically-generated name.  This can happen if the script is run more than once.  Delete the Monitor name before you run this script a 2nd time.
 
 > **Note** The automatic script expects that a **Production** Deployment is being used.  This happens automatically if using the results of the Pipeline execution as described in this example.  If another Deployment is used, ensure that it has been deployed for Production.

 - From the JupyterLab tab, navigate to folder <code>/workspace/**\<your-code-repo\>**/insurance/monitoring</code>
 - Open `modelmonitor.iypnb` <br><br>
   > **Warning** Ensure that the last cell at the bottom of the file has `CLEANUP = False`  This may have been set to `True` from a previous execution.
  - Run all of the cells
 - This will create a new Model Monitor and put it into the `Active` state
   - The Monitor name will be the same as the Deployment name <br><br>
 - Navigate to the `Deployments` menu on the left
 - Select the `Monitors` tab at the top
 - You will see the new Monitor at the top of the list

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

## Cleanup
 After the experiment is complete, the following cleanup should be performed in order to delete the Datasets and stop the Monitor:
 
 - Within `modelmonitor.ipynb`, set the variable `CLEANUP = True` in the last cell
   - Run the "Cleanup" cell
   - Do not execute the next step until this step has completed
 - Within `resources.ipynb`, set the variable `CLEANUP = True` in the last cell
   - Run the "Cleanup" cell


