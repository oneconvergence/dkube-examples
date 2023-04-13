# Chest X-Ray Image Monitor Example (UI-Based Workflow)

This example trains a model to identify pneumonia from chest x-rays.  The model is then deployed and used as the basis for monitoring with synthetic live data to demonstrate the DKube monitoring capability.

This workflow uses a Kubeflow Pipeline to set up the resources and created the monitor.  A separate readme file is available in this folder to create the monitor through JupyterLab scripts, in the same folder called [README-monitor-nb.md](README-monitor-nb.md)

- This example supports model deployment with a full DKube cluster (`serving cluster`) and model monitoring on either the same cluster or a seperate minimal DKube cluster (`monitoring cluster`).
  - **Serving cluster:** Where the production deployment will be running
  - **Monitoring cluster:** Where the model monitor will be running
  > **Note**: The serving and monitoring clusters can be same, but in that case the setup has to be a single **full** DKube setup

## Example Flow

- Create the necessary DKube resources
- Train and deploy a model
- Create a monitor
- For seperate serving and monitoring clusters
  - Add a serving cluster link on the monitoring cluster
  - Import the deployment onto the monitoring cluster
- Generate data for analysis by the monitor
  - Predict data: Inference inputs/outputs
  - Label data:  Dataset with Groundtruth values for the inferences generated above
  > **Note** In a production environment, the label data would be manually generated by experts in the domain.  In this example, we are creating the labeled data automatically.
- Cleanup the resources after the example is complete

## 1. Create DKube Code Repo

The DKube Code repo is required for the initial setup scripts to execute.  

> **Note** If this was already done, skip this section and move on to `Section 2`.  Otherwise, follow the instructions in this section.

- Select `Code` menu on the left, then `+ Code`, and fill in the following fields:
  - **Name:** `chest-xray`  **(Or choose your own name as `<your-code-repo>`)**
  - **Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples.git`
  - **Branch:** `monitoring`
- Leave the rest of the fields at their current value
- `Add Code`

## 2. Create and Launch JupyterLab

In order to run the script to set up the resources, and to train and deploy the model, a JupyterLab IDE needs to be created.  The scripts will be run from within JupyterLab.  

> **Note** If the JupyterLab notebook has already been created, go directly to `Section 3` to create the resources.  Otherwise, follow the instructions in this section.

- Select `IDE` menu on the left, then `+ JupyterLab`, and fill in the following fields:
  - **Name:** *`<your-IDE-name>`*  **(Choose a name)**
  - **Code:** *`<your-code-repo>`*  **(Chosen during Code repo creation)**
  - **Framework:** `tensorflow`
  - **Framework Version:** `2.0.0`
  - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-17`   **(This should be the default, but ensure that it is selected)**
- Leave the rest of the fields at their current value
- `Submit`

## 3. Create the Resources

- Once the IDE is running, launch JupyterLab from the icon on the far right
- Navigate to <code>workspace/**\<your-code-repo\>**/chest-xray</code>
- Open `resources.ipynb`
> **Warning** Ensure that `Cleanup = False` in the last cell, since it may have been changed in a previous execution

- If you called your code repo something other than `chest-xray`, edit the following variable in the 3rd cell labeled `User-Defined Variables`:
  - `DKUBE_TRAINING_CODE_NAME` = *`<your-code-repo>`*

### Serving and Monitoring on Same Cluster

- If the serving and monitoring cluster are the same, no other fields need to be changed, skip to [Run the Script](#run-the-script)

### Serving and Monitoring on Different Clusters

- If the monitoring cluster is separate from the serving cluster, you need to provide more information for cluster communication
  - `SERVING_CLUSTER_EXECUTION` = `False`
  - `SERVING_DKUBE_URL` = DKube access URL for the serving cluster, with the form
    - `https://<Serving Cluster Access IP Address>:32222/`
    > **Note** Ensure that there is a final `/` in the URL field
  - `MONITOR_DKUBE_URL `= DKube access URL from the monitoring cluster, with the form
  - `MONITORING_DKUBE_USERNAME` = Username on the monitoring cluster
  - `MONITORING_DKUBE_TOKEN` = Authentication token from the monitoring cluster, from the `Developer Settings` menu
    - `https://<Monitor Cluster Access IP Address>:32222/`
    > **Note** Ensure that there is a final `/` in the URL field
- If the Monitoring cluster already has a link to the Serving cluster from the DKube Clusters Operator screen
  - Get the name of the DKube cluster link and provide that name to the variable `SERVING_DKUBE_CLUSTER_NAME` <br><br>
- If the Monitoring cluster link has not been created by the Operator on the Monitoring cluster:
  - Leave the variable `SERVING_DKUBE_CLUSTER_NAME = ""`
  - In that case, the link will be created on the Monitoring cluster
  - The username identified in the `MONITORING_DKUBE_USERNAME` variable must have Operator privileges for this to work. If not, the script fill fail.
  - Leave the other fields at their current value

### Run the Script

- `Run` > `Run All Cells` from the top menu <br><br>
- The following resources will be created:
  - `chest-xray` Dataset on both the serving and monitoring cluster
  - `<your user name>-image-mm-kf` Model on the serving cluster
  - `<your user name>-image-mm-kf-s3` Dataset on the monitoring cluster

## 4. Train and Deploy the Model on Serving Cluster

In order for the monitor example to operate, a model must be trained and deployed on the serving cluster.  A Kubeflow Pipeline executes this step.

> **Note** If the deployed model has already been created, skip to `Section 5` to create the monitor.  Otherwise, follow the instructions in this section.

- Open `train.ipynb`
- `Run All Cells`
- This creates and executes a pipeline in order to:
  - Preprocess the dataset and generate the training data or retraining data
  - Train with the generated dataset as an input, and create an output model
  - Deploy the generated model on a predict endpoint
- The pipeline will create a new version of the Model `image-mm-kf`
> **Note** Wait for the pipeline to complete before continuing

- After the pipeline is complete, and the deployed model has been created on the serving cluster, select the 2nd from the last cell in the `train.ipynb` script and `Run Selected Cell` (not "Run All Cells")
- This will provide information that is necessary when configuration the monitor in this example.  They are available in the 2nd to last cell, labeled `Fields Used for Configuring the Monitor through the UI`.  They will be referenced in the Drift & Performance configuration sections.

<img src="./Screenshots/Resources_Image.png" width=100% height=100%>

## 5. Import Serving Deployment if Monitoring on a Separate Cluster

> **Note** If the Monitor is on the Serving cluster, skip to `Section 6` and create the monitor.  Otherwise, follow this section to import the deployment.

If the Monitor is on a different cluster than the Served deployment, the deployment first needs to be imported to the Monitor cluster. In order for this to work, a `Cluster` link needs to be set up from the Monitor to the Serving cluster.  This is done by a user with Operator authorization.

> **Note** These steps are performed on the `Monitoring` cluster

- Navigate to the `Deployments` menu on the left
- Select `+ Import` and fill in the following fields:
  - **Name:** `image-mm-kf`
  > **Note** This is the name of the deployed model on the Serving cluster
  - **Cluster:** `Cluster name previously set up for the Serving cluster`
  - **Namespace:** `User name on the Serving cluster`
- Leave the other fields at their current selection
- `Import`

## 6. Create Model Monitor

This section describes the process to create and activate a monitor.

> **Note** These steps are performed **on the cluster where the monitor will run**, either:

- Serving cluster (if the deployment and monitor are on the same cluster)
- Monitor cluster (if the monitor is on a different cluster than the deployment)

There are 4 basic setups screens to configure:

- `Settings`
  - Provides overall comfiguration information on the type of monitor, such as what type of model it is and the data type
- `Health`
  - <onitors the deployment health, and is enabled by default with minimal configuration required
- `Drift`
  - Sets up Data Drift configuration for inputs and outputs
- `Performance`
  - Sets up Performance Decay configuration, which must include the ground truth

Follow the instructions in this section to setup the basic monitor

- Navigate to the `Deployments` menu on the left
- Select the `Add Monitor` icon on the far right of the deployment row
- Fill in the following fields:
  - `Settings` tab
    - **Model Type:** `Classification`
    - **Input Data Type:** `Image`
  - Leave the other fields at their current selection <br><br>
  - `Drift` tab
    - Check `Enable`
    - **Algorithm:** `Auto`
    - **Image Shape** 
      - **Height:** `200`
      - **Width:** `200`
      - **Channel:** `1`
      - **Channel Order:** `Channels Last`
    - **Train Data**
      - **Dataset:** `chest-xray`
      - **Dataset Version:** `v1`
      - **Images Saved As:** `Images in labelled folder`
    - **Predict Data**
      - **Dataset Content:** `CloudEventlogs` <br><br>
      - If the monitor is on the **same cluster** as the served model, there there is no more configuration for the `Drift` tab
      - If the monitor is on a **different cluster** than the served model, there will be 2 more fields in this tab
        - **Dataset:** `image-mm-kf-s3`
        - **Prefix/Subpath:** `<Deployment ID of Served Model>
        > **Note** The deployment ID of the served model is available from the `train.ipynb` run as described at the end of `Section 4`
  - Leave the other fields at their current selection <br><br>
  - `Performance` tab
    - Check `Enable`
    - **Compute Metrics:** `Labelled Data`
    - **Dataset":** `image-mm-kf-s3`
    - **Prefix/Subpath:** <code>\<Deployment ID of Served Model\>/**livedata**</code>
    > **Note** The deployment ID of the served model is available from the `train.ipynb` run as described at the end of `Section 4`
    - **Groundtruth Column Name:** `label`
    - **Prediction Column Name:** `output`
    - **Timestamp Column Name:** `timestamp`
  - Leave the other fields at their current selection
- `Submit`
  - Choose `Close` from the popup

## 7. Configure Schema

After the model monitor has been configured, the Schema needs to be completed to identify the input and output types.  

- Navigate to the `Deployments` menu on the left
- Select the `Monitors` tab on the top
- The newly created Monitor will show up on the list
  - The Monitor will be in the `pending` status. If it is not yet at that status, wait until it is.
- Select the `Update Schema` icon from the `Actions` column on the right of the monitor row
  - The Schema window will appear
- Select the `+ Add` button
  - **Name:** `prediction`
  - **Column/Feature Type:** `Prediction Output`
  - **Value Type:** `Categorical`
  - Select `Add`
  - `Close`

## 8. Add Alert

Alerts will provide a notification that there is a potential issue.

- Navigate the `Deployments` > `Monitors` screen
- Select the `Add Alerts` icon from the `Actions` column on the right of the monitor row
- Select `Add Alert` and fil in the following fields:
  - **Alert Name:** `accuracy`
  - **Alert Type:** `Performance Decay`
  - **Configure Based On:** `Threshold`
  - **Add Metric**
    - `accuracy` | `<` | `0.85`
- Leave the other fields at their current selection
- `Submit`

## 9. Upload Thresholds

Thresholds provide the soft and hard limits that drive the status indications for the monitor.  You upload a threshold file that sets them up.

- Get the thresholds file from https://github.com/oneconvergence/dkube-examples/tree/monitoring/image_cloudevents/threshold.json
  - Select the `Raw` button
  - Right click and `Save as...` <br><br>
- Navigate the `Deployments` > `Monitors` screen
- Select the `Upload Thresholds` icon from the `Actions` column on the right of the monitor row
  - Select `Upload `
  - `View` the file
  - `Submit`

## 10. Start Monitor

The Monitor needs to be in the `active` state to execute the monitoring function.

- Navigate to the `Deployments` > `Monitors` screen
- Ensure that the Monitor is in the `ready` state
  - If not, do not proceed, since something has not been properly configured
- Select the Monitor with the checkbox to the left
  - Select `Start` button <br><br>
- The details of how to view and understand the Monitor are described at [DKube Monitor Dashboard](https://dkube.io/monitor/monitor3_x/Monitor_Workflow.html#monitor-dashboard)
