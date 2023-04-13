# Chest X-Ray Example

This example trains a model to identify pneumonia from chest x-rays.

## Example Flow

- Create the necessary DKube resources
- Launch a JupyterLab notebook to experiment with your code
- Compare the model metrics
- Deploy a model for serving
- Train a model with hyperparameter optimization

If you want to create a Model Monitor, you can follow the steps at [Create a Model Monitor](./README-monitor-nb.md).

## 1. Create the DKube Repos

DKube Repos provide a convenient way to use the example within a notebook and for your batch training runs.

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

You can view and experiment with your code using JupyterLab.

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

## 3. Experiment with your code

Once the JupyterLab instance is running, open a new tab using the icon at the far right of the instance.

- Navigate to <code>workspace/**\<your-code-repo\>**/chest-xray</code>
- Open `training-notebook.ipynb`
- `Run all cells` <br><br>
- You can change the number of `epochs` or `learning rate` in "cell [3]: Hyperparamters" and rerun the script

## 4. Create a Trained Model

A batch training run creates a model.

- Select `Runs` menu on the left, then `+ Run / Training`, and fill in the following fields:
  - **Basic Tab**
    - **Name:**  `Choose a Run name as <your-run-name>`
    - **Code:** *`<your-code-repo>`*  **(Chosen during Code repo creation)**
    - **Framework:** `tensorflow`
    - **Framework Version:** `2.0.0`
    - **Image:** `ocdr/dkube-datascience-tf-cpu:v2.0.0-xx`   **(This should be the default, 'xx' may differ)**
    - **Start-up command:** `python chest-xray/training.py` <br><br>
  - **Repos Tab**
    - **Inputs / Datasets:** *`<your-dataset-repo>`*   **(Chosen during Dataset repo creation)**
      - **Mount Path:** `/data`
    - **Outputs / Models:** *`<your-model-repo>`*   **(Chosen during Model repo creation)**
      - **Mount Path:** `/model`
    > **Note** Ensure that you select the `Output Models` section, and not the `Input`
- Leave the rest of the fields at their current value
- `Submit`

## 5. Clone a Run and Train a 2nd Model

- Select `Runs` menu on the left
- Select *`<your-run-name>`*
  > **Note** There may be other Runs, but choose the one that you created
- Select `Clone` from the top menu
- Fill in the following fields:
  - **Basic Tab**
    - **Name:** `Choose a new name`
    - Leave the rest of the Basic fields at their current value<br><br>
  - **Configuration Tab**
    - Select `Environment variables` by choosing the `+` button on the right
      - **Key:** `EPOCHS`  **(Must be in all caps)**
      - **Value:** `10`
- Leave the rest of the fields at their current value
- `Submit`

## 6. Compare the Trained Models

This section uses the Model versions from the Training Runs to compare metrics.

- Wait for all Runs to complete
- Select `Models` on the left menu
- Select *`<your-model-repo>`* by expanding the caret `>` on the left
- Select the checkboxes for the v2 & v3 of the Model  (The first version is a placeholder)
- Select `Compare` button at the top
  - Scroll to the `Y-axis` field to the left of the graph
  - Select `train_accuracy`
  - The graph will show the training accuracy of each Run <br><br>
- Go back to the previous screen by using the breadcrumb `<-` at the top left
- Expand the Model
- Choose `v2` by clicking on the name
- Select the `lineage` tab
- This shows the inputs and outputs of the Run that created this Model

## 7. Deploy a Model

This section deploys a Model for serving.

- Select `Models` on the left menu
- Select *`<your-model-repo>`* by clicking on the name
- Choose the `Deploy` icon at the far right of `v3` and fill in the following fields
  - **Name:** `Choose a name`
  - **Deployment:** `Production`
  - **Deploy Using:** `CPU`
- Leave the rest of the fields at their current value
- `Submit` <br><br>
- Select `Deployments` on the left menu to view the new deployment

## 8. Execute a Katib Run

This section trains a Model using using Katib-based hyperparameter optimization

- Download the hyperparameter optimization file from [Katib Tuning File](https://github.com/oneconvergence/dkube-examples/tree/training/chest-xray/xray-tuning.yaml)
  - Select `Raw`
  - Right-click on the file and use `Save as...` <br><br>
- Select the `Runs` menu on the left
- Choose the first Run
- Select the Run checkbox and `Clone` on the top menu screen menu
  - **Name:** `Choose a name`
  - Select the `Configuration` tab
  - Delete any `Environmental variables` using the `X` on the right
  > **Note** This step is important, since the Katib run will not work properly with variables active
  - Select the `Upload` button on the `Upload Tuning Definition` section
  - Choose the Katib file that you downloaded
- `Submit` <br><br>
- When the Run is complete, a single Model will be created with the best trial
- You can view the results by selecting the Katib icon on the far right of the Run

## 9. Create Resources for Pipeline and Monitor

This section sets up the resources and global variable definitions to enable a Pipeline Run and Model Monitor.

- Within the `JupyterLab` tab, open `resources.ipynb`
- Change the following variables in the 3rd cell `User-Defined Variables`
  - DKUBE_TRAINING_CODE_NAME = `<your-code-repo>`
  - TRAINING_DATASET = `<your-dataset-repo>`
  - DKUBE_MODEL_NAME = `<your-model-name>`
  - Leave the other variables at their current value
- `Run All Cells`

## 10. Run a Kubeflow Pipeline

This section executes a Pipeline to train and deploy a model.

- Within the `JupyterLab` tab, open `train-and-deploy.ipynb`
- `Run all Cells` <br><br>
- Select `Pipelines` on the left menu
- Select `Runs` tab on the top

You will see your Pipeline listed as being executed.  When the Pipeline is complete, both steps will have a green checkmark.

- Select the `Deployments` menu on the left
- Your new Deployment will appear, with the name `<your-user-name>-chest-xray`

> **Note** You can create a Model Monitor by following the steps at [Create a Model Monitor](./README-monitor-nb.md)

  
