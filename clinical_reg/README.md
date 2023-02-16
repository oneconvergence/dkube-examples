# Clinical Regression Example
 
This example takes clinical data, RNA data, and images as inputs and uses regression to train a model that will predict how long the person is expected to take to recover.  The training flow is:

- Preprocess the clinical data and images
- Split the training data into training, validation, and test datasets
- Train the model
- Deploy the model
- Test the model with a WebApp

 This example provides a fully automated way to train and deploy the model.

## 1. Create Code Repo

The Code Repo contains the program code and other associated files for developing and running your model training.

- Navigate to `Code` menu on the left side of the screen
- Select `+ Code`
  - **Name:** `regression`
  - **Code Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples.git`
  - **Branch:** `tensorflow`
  - Leave the other fields in their current selection and `Submit`

## 2. Automated Setup and Execution using Kubeflow Pipelines

 The clinical regression can be run in an automated manner through a Kubeflow Pipeline.

### Create JupyterLab IDE

 A JupterLab IDE is used to create the pipeline that trains the model.

 - Navigate to `IDEs` menu on the left
 - Select `+ JupyterLab`
   - **Name:** `<your-ide-name>`  **(Your choice of name)**
   - **Code:** Select `regression`
   - **Framework:** `Tensorflow`
   - **Framework Version:** `2.0.0`
   - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-17`
   > **Note** The image should default to the correct selection, but you should check to ensure that it is the right one
   - Leave the other fields in their current selection and `Submit`

### Create & Run Pipeline

 A JupyterLab script is used to create the training pipeline.

 - Navigate to `IDEs` menu on the left
 - When the JupyterLab instance is running, select the icon on the right to open a new JL tab
 - Navigate to <code>workspace/regression/clinical_reg</code>
 - Open `pipeline.ipynb`
 - Select `Run` menu at the top and Select `Run All Cells` <br><br>
 - This will create the Kubeflow Pipeline to:
   - Create the datasets
   - Proprocess the data
   - Split them in to train, validate, & test
   - Train the model
   - Deploy the model
   - Start the inference WebApp <br><br>
 - The pipeline will be automatically created within DKube, and a pipeline run will be started <br><br>
 - Navigate to `Pipelines` menu to view the pipeline graph and track the progress
 - Select `Runs` tab on the top
 - Your new pipeline run will be the first entry
 - Select `View Pipeline` on the Run row to see the entire pipeline
 - Use the backarrow to view the list of pipelines again
 - Select the pipeline name to view the pipeline progress

### View Resources Created by Pipeline

 After the pipeline has completed its execution, you can view the Runs, Datasets, and Models created.  You can go to the `Test Inference` section to use example files with the deployed model.

## 3. Test Inference

 One Convergence has created a simple test inference application for this example.

 - From the JupyterLab tab, download the csv data file `cli_inp.csv` from the `./sample_data` folder, and any sample image from the `./sample_data/images` folder
 - Navigate to the `Deployments` menu on the left and identify the deployment from the pipeline (it should be at the top)
   - Copy the `Endpoint` URL from that row to your clipboard using the icon
 - In a new tab, access the WebApp at `https://<your-dkube-url>/inference`  (Eg. `https://1.2.3.4:32222/inference`)
 - In the WebApp, fill in the following fields:
   - Paste the `Endpoint` URL into the `Model Serving URL` field
   - Copy the token from the DKube `Developer Settings` menu at the top right
   - Select the model type as `Regression`
   - Select `Upload Image` and use the image file that you downloaded
   - Select `Upload File` and use the csv file that you downloaded
   - `Predict` <br><br>
 - The WebApp will predict how long the person will take to recover
 > **Note** You may receive a message that the WebApp has timed out.  This is due to the pod starting up.  Select `Wait`.

<!---

This section will not be used, but is kept here in case it is needed later.

## 4. Manual Development with Example

Once the pipeline has created the resources, you an use DKube to perform the steps manually in order to understand the flow.

### Create a JupyterLab Notebook with Datasets Mounted

In order to perform the manual workflow, a new JupyterLab notebook needs to be created and launched with the datasets and mount points added.

- Navigate to `IDEs` menu on the left
- Select `+ JupyterLab`
- `Basic` tab
  - **Name:** `<your-ide-name>`  **(Your choice of name)**
  - **Code:** Select `<your-code-repo>`  **(From the Code Repo selection step)**
  - **Framework:** `Tensorflow`
  - **Framework Version:** `2.0.0`
  - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-17`
  > **Note** The image should default to the correct selection, but you should check to ensure that it is the right one <br><br>
- `Repos` tab
  - `Inputs` > `Datasets`
    - `clinical`
      - **Mount Path:** `/opt/dkube/input/clinical`
    - `images`
      - **Mount Path:** `/opt/dkube/input/images`
    - `rna`
      - **Mount Path:** `/opt/dkube/input/rna` <br><br>
- Leave the other fields in their current selection and `Submit`

### Experiment with Training using JupyterLab

The JupyterLab notebook allows you to see the steps in the workflow, and to experiment with different parameters.

- When the JupyterLab notebook instance is running, open a new tab by selecting the icon on the right of the row
- Navigate to <code>workspace/**\<your-code-repo\>**/clinical_reg</code>
- Open `workflow.ipynb`
  - `Run All Cells` <br><br>
- The notebook file goes through the experiment steps
  - Preprocess & visualize the data
  - Split the data into train, validation, & test datasets
  - Train on the data
  - Save the model
  - Compare the models

### Train Model with Batch Run

A batch training run will create a model that can be used to analyze the metrics.  The training assumes that the datasets have been preprocessed by the initial pipeline.

- Navigate to `Runs` menu on the left, select `+ Run` > `Training` and fill in the following fields:
- `Basic` tab
  - **Name:** `<your-run-name>`  **(Your choice of name)**
  - **Code:** Select `<your-code-repo>`  **(From the Code Repo selection step)**
  - **Framework:** `Tensorflow`
  - **Framework Version:** `2.0.0`
  - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-17`
  > **Note** The image should default to the correct selection, but you should check to ensure that it is the right one
  - **Startup Command:** `python workflow.py` <br><br>
- `Repos` tab
  - `Inputs` > `Datasets`
    - `clinical`
      - **Mount Path:** `/opt/dkube/input/clinical`
    - `images`
      - **Mount Path:** `/opt/dkube/input/images`
    - `rna`
      - **Mount Path:** `/opt/dkube/input/rna` <br><br>
  - `Outputs` > `Models`
    - `regression-model`
      - **Mount Path:** `/opt/dkube/output`
  > **Note** Ensure that you enter the Model information into the `Outputs` section and **not** the `Inputs` section
- Leave the other fields in their current selection and `Submit` <br><br>
- This will start a Training Run, which will create a Model when it is complete

### Compare the Model Metrics

Each training run will create a model.  The metrics from the model can be compared to determine the best model for deployment.  With the original pipeline run and the manual run, there will be models that can be compared.

- Navigate to the `Models` menu on the left
- Open `regression-model` with the `>` to the left
- Choose the most recent 2 versions
- Select `Compare` button at the top
  - View the metrics in a tabular form at the top of the screen
  - Scroll down to the graph and in the `Y-Axis` screen select `train_loss`
  - The graph will show the difference between the models in graphical form <br><br>
- Navigate back to the model list with the back arrow `<--` at the top
- Select the `regression-model` name (**not** the caret)
- Select the newest version
- Select the `lineage` tab at the top of the next screen
  - View the inputs and output that created this model
  - This can be used to improve the model if required

### Deploy the Model

Once the model with the best metrics has been identified, it can be deployed for live inference serving.

- Navigate to the top of the `Models` menu
- Select the `regression-model` name
- Select the `Deploy` icon on the far right of the newest version, and fill in the following fields:
  - **Name:** `<your-deploy-name>`   **(Choose a name)**
  - **Deployment:** `Test`
  - **Deploy Using:** `CPU`
  - Select `Transformer` checkbox
  - **Transformer Script:** `clinical_reg/transformer.py`
- Leave the other fields in their current selection and `Submit` <br><br>
- Navigate to the `Deployments` menu
- Your new model will be deployed on this screen
- You can test the deployment with the WebApp as described above

--->