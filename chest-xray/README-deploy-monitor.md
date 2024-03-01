# Chest X-Ray Example (Deploy and Monitor)

This example deploys a model and creates a monitor.

## 1. Create the DKube Repos

### Create a repo for the Code

- Select `Code` menu on the left, then `+ Code`, and fill in the following fields:
  - **Name:** `chest-xray`  **(Or choose your own name as `<your-code-repo>`)**
  - **Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples.git`
  - **Branch:** `training`
- Leave the rest of the fields at their current value
- `Add Code`

### Create a repo for your Datasets

- Select `Datasets` menu on the left, then `+ Dataset`
  - **Name:** `chest-xray` **(Or choose your own name as `<your-dataset-repo>`)**
  - **Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples/tree/training/chest-xray/data/chest-xray-mini`
- Leave the rest of the fields at their current value
- `Add Dataset`

### Create a repo for your Model

- Select `Models` menu on the left, then `+ Model`
  - **Name:** `chest-xray`  **(Or choose your own name as `<your-model-repo>`)**
- Leave the rest of the fields at their current value
- `Add Model`

## 2. Create and Launch JupyterLab

- Select `IDEs` menu on the left, then `+ JupyterLab`, and fill in the following fields:
  - **Basic Tab**
    - **Name:** `Choose an IDE name`
    - **Code:** *`<your-code-repo>`*  **(Chosen during Code repo creation)**
    - **Framework:** `tensorflow`
    - **Framework Version:** `2.0.0`
    - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-xx`   **(This should be the default, 'xx' may differ)**
    - Leave the rest of the Basic fields at their current value<br><br>
  - **Repos Tab**
    - **Inputs / Datasets:** *`<your-dataset-repo>`*   **(Chosen during Dataset repo creation)**
      - **Mount Path:** `/data`
- Leave the rest of the fields at their current value
- `Submit`

## 3. Create Resources for Pipeline and Monitor

This section sets up the resources and global variable definitions to enable a Pipeline Run and Model Monitor.

- Within the `JupyterLab` tab, open `resources.ipynb`
- Change the following variables in the 3rd cell `User-Defined Variables`
  - DKUBE_TRAINING_CODE_NAME = `<your-code-repo>`
  - TRAINING_DATASET = `<your-dataset-repo>`
  - DKUBE_MODEL_NAME = `<your-model-name>`
  - Leave the other variables at their current value
- `Run All Cells`

## 4. Train and Deploy a Model

- Within the `JupyterLab` tab, open `train-and-deploy.ipynb`
- `Run all Cells` <br><br>
- Select `Pipelines` on the left menu
- Select `Runs` tab on the top

You will see your Pipeline listed as being executed.  When the Pipeline is complete, both steps will have a green checkmark.

## 5. Clone a Run and Train a Model

- Select `Runs` menu on the left
- Select the Run created from the Pipeline, of the form `<your-code-repo>-pl-xxxx`
  > **Note** There may be other Runs, but choose this one as your base
- Select `Clone` from the top menu
- Fill in the following fields:
  - **Basic Tab**
    - **Name:** `Choose a new name`
    - Leave the rest of the Basic fields at their current value<br><br>
- Leave the rest of the fields at their current value
- `Submit` <br><br>
- Wait for training run to complete

## 6. Deploy a Model

- Select `Models` on the left menu
- Select *`<your-model-repo>`* by clicking on the name
- Choose the `Deploy` icon at the far right of `v3` and fill in the following fields
  - **Name:** `Choose a name`
  - **Deployment:** `Production`
  - **Deploy Using:** `CPU`
- Leave the rest of the fields at their current value
- `Submit` <br><br>
- Select `Deployments` on the left menu to view the new deployment

## 7. Create a Model Monitor

In order to monitor the deployed model, a monitor is created and launched.  This workflow executes this programatically through the DKube SDK. This can also be done through the UI by following a different example flow in this repo.

> **Note** The Monitor will use the Deployment that was created from the `train-and-deploy` script

- Open `modelmonitor.ipynb`
 
> **Warning** Ensure that `Cleanup = False` in the last cell, since it may have been changed in a previous execution
 
- `Run all Cells`
- This script will:
  - Add the right links and import the deployment if the monitoring is on a different cluster from the serving cluster
  - Create a new model monitor
- After the script has completed, the monitor `<your-user-name>-chest-xray` will be in the active state

## 8. Generate Data

Predict and Groundtruth datasets will be generated by this script, and will be used by the monitor to analyse the model execution.

- Open `data_generation.ipynb`
- In the 1st cell, update the number of data generation cycles to complete
  - `Run All Cells`