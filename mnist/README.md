# MNIST DIGITS CLASSIFICATION EXAMPLE 

 This example uses the `mnist` model to identify a digit from an image.  It steps through a simple DKube workflow.

 > **Note** This example runs on DKube V3.x and above

## 1. Setup Resources

 Before using DKube to experiment, train, and deploy, the resources must be set up.

### Create Code Repo

 - From the `Code` menu on the left, select `+ Add Code` with the following fields:
   - **Name:** `mnist`  **(Or choose `<your-code-repo>`)**
   - **Code Source:** `Git`
   - **URL:**: `https://github.com/oneconvergence/dkube-examples.git`
   - **Branch:** `tensorflow`
 - Leave the other fields in their current selection and `Add Code`

### Create Dataset Repo

 - From the `Datasets` menu, select `+ Add Dataset` with the following fields:
   - **Name:** `mnist`  **(Or choose `<your dataset-repo`)**
   - **Dataset source:** `Other`
   - **URL:** `https://s3.amazonaws.com/img-datasets/mnist.pkl.gz`
 - Leave the other fields in their current selection and `Add Dataset`  

### Create Model Repo

 - From the `Models` menu, select `+ Add Model` with the following fields:
   - **Name:** `mnist`  **(Or choose `<your model-repo`)**
 - Leave the other fields in their current selection and `Add Model`  

## 2. Create & Launch JupyterLab Notebook

 JupyterLab can be used to experiment with your code.

 - Ensure that all of Repos above are in the `Ready` state
 - From the `IDEs` menu, select `+ Add JupyterLab` with the following fields:
   - `Basic` tab
     - **Name:** `<your-IDE-name`  **(Your choice)**
     - **Code:** `<your-code-repo>`  **(Created during the Code Repo step)**
     - **Framework:** `tensorflow`
     - **Framework Version:** `2.0.0`
     - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-17`
     > **Note** The default Tensorflow Image should fill in automatically, but ensure that it is correct <br><br>
   - `Repos` tab
      - **Inputs** > **Datasets**: `<your-dataset-repo>`  **(Created during the Dataset Repo step)**
        - **Mount Path:** `/mnist`
 - Leave the other fields in their current selection and `Submit` <br><br>
 - Once the IDE is running and the JupyterLab icon on the right is active, select it to launch a JupyterLab window
   - Navigate to <code>workspace/**\<your-code-repo\>**/mnist</code>
   - Open `train.ipynb`
     - `Run All Cells` from the menu at the top
     - Change the `EPOCHS` variable in the 2nd cell "5" and rerun all cells
     - You can view the difference in output at the bottom of the script
     > **Note** You would normally be developing your code in JupyterLab, and once you were satisfied you would create a Python file from the `ipynb` file.  In this example, a Python file is already ready for execution.

## 3. Work with Training Runs

 Batch training runs can be used to create trained models.

### Run Training Job

- From the `Runs` menu, select `+ Run` > `Training` with the following fields:
   - `Basic` tab
     - **Name:** `<your-run-name`  **(Your choice)**
     - **Code:** `<your-code-repo>`  **(Created during the Code Repo step)**
     - **Framework:** `tensorflow`
     - **Framework Version:** `2.0.0`
     - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-17`
     > **Note** The default Tensorflow Image should fill in automatically, but ensure that it is correct <br><br>
     - **Start-up Command:** `python mnist/train.py`
   - `Repos` tab
      - **Inputs** > **Datasets**: `<your-dataset-repo>`  **(Created during the Dataset Repo step)**
        - **Mount Path:** `/mnist` <br><br>
      - **Outputs** > **Models**: `<your-model-repo>`  **(Created during the Model Repo step)**
        - **Mount Path:** `/model`
      > **Note** Ensure that you add the Model into the `Outputs` section, and not the `Inputs` section
   - Leave the other fields in their current selection and `Submit`
   - Your Run will show up from the `Runs` menu screen <br><br>
   - Clone the Run by selecting the checkbox and choosing `Clone` from the top buttons
     - Leave the `Basic` and `Repos` tabs the same
     - On the `Configuration` tab
       - Select the `+` button next to `Environment Variables`
       - **Key:** `EPOCHS`   **(Must be in upper case)**
       - **Value:** `5`
     - `Submit`

### Compare Runs

 - Wait for both Runs to `complete`
 - From the `Runs` menu, select both Run checkboxes, then select `Compare` button
 - Scroll down and choose **Y-Axis:** `train_accuracy`

### Run Katib-Based Hyperparameter Tuning
 
 - Go to https://github.com/oneconvergence/dkube-examples/tree/tensorflow/mnist/tuning.yaml
 - Select `Raw`
 - Right-click & `Save as...` "tuning.yaml" <br><br>
 - From the `Runs` menu, select the first Run checkbox, then select `Clone`
   - Leave the `Basic` and `Repos` tabs the same
   - On the `Configuration` tab
     - Select `Upload Tuning Definition`
     - Choose the `tuning.yaml` file that you saved
   - `Submit` <br><br>
 - Wait for Run to complete
 - View the results by selecting the Katib icon on the right of the Run line

#### Tuning.yaml File Details

 - **objective**: The metric that you want to optimize
 - **goal** parameter is mandatory in tuning.yaml file
 - **objectiveMetricName:** Katib uses the objectiveMetricName and additionalMetricNames to monitor how the hyperparameters work with the model. Katib records the value of the best objectiveMetricName metric.
 - **parameters** : The range of the hyperparameters or other parameters that you want to tune for your machine learning (ML) model
 - **parallelTrialCount**: The maximum number of hyperparameter sets that Katib should train in parallel. The default value is 3.
 - **maxTrialCount**: The maximum number of trials to run
 - **maxFailedTrialCount**: The maximum number of failed trials before Katib should stop the experiment
 - **algorithm**: Search algorithm to find the best hyper parameters. Value must be one of following:
   - random
   - bayesianoptimization
   - hyperband
   - cmaes
   - enas

## 4. Deploy Model

 After the best model is identified, it can be deployed for inference serving.

- From `Models` menu, select `<your-model-repo>`  **(Created during Model Repo step)**
- Choose the highest version of the Model
- Select the `Lineage` tab
  - This provides information on the inputs and outputs of the Model <br><br>
- Select the `Metrics` tab
  - This provides the metrics associated with the Model <br><br>
- Go back to `Models` top menu, and reselect the Model
- Select the `Deploy` icon on the right of the newest Model
  - **Name:** `<your-deploy-name>`  **(Your choice)**
  - **Deployment:** `Production`
  - **Deploy Using:** `CPU`
  - **Transformer:** `Check Box`
    - **Transformer Script:** `mnist/transformer.py`
  - Leave the other fields in their current selection an `Submit` <br><br>
  - The deployed Model will appear in the `Deployments` menu screen

## 5. Train & Deploy with Kubeflow Pipelines

 The training and deployment steps can be automated using Kubeflow Pipelines.

 - Open the JupyterLab window
 - Navigate to <code>workspace/**\<your-code-repo\>**/mnist</code>
 - Open `pipeline.ipynb` <br><br>
 - If you chose the default value for all of your repos (`mnist`) then `Run all Cells`<br><br>
 - If you chose different repo names
   - In the 2nd cell, labeled `User Variables`, modify the repo names with your chosen names
   - `Run All Cells` from the menu at the top <br><br>
 - From the `Pipelines` menu on the left
   - Select `Runs` tab
   - Your new pipeline will be executing
   - Select the pipeline name to see its progress

## 6. Test inference

 - Create a browser tab and go to https://<dkube_url>/inference
 - Paste the Endpoint URL from `Deployments`
 - Copy Auth token from `Developer settings` in DKube page and paste in
 - Choose `mnist` for model type
 - Download `3.png` from repo
 - Click `Predict`
 > **Note** The prediction may time out waiting for the pod to start - select `wait` if prompted
