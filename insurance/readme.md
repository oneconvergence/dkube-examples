# Insurance Cost Prediction Example
 This example trains a model to predict the cost of insurance based on a set of input characteristics for an individual.  This description provides a step-by-step recipe for using the example.  More details for the platform are available at [DKube User Guide](https://www.dkube.io/guide/guide3_x/Getting_Started.html) <br><br>
 This example contains the following capabilities:  
 
 - Create the Repos required for training
 - Create and experiment with a JupyterLab IDE
 - Create and run Training Jobs and compare their output metrics
 - Submit and review a Katib-based Hyperparameter optimization job
 - Deploy a Model for inference serving
 - Create a Kubeflow Pipeline
 - Create and start a Model Monitor for a deployment
   - The instructions for the monitoring section of this example are available in the "/monitoring" folder

 > **Note** In the example, use only lower-case characters in the names that you create. Hyphens are acceptable in any position **other than** the first and last characters, but no other special characters should be used.

> **Note** You can choose the names for your resources in most cases.  It is recommended that you choose names that are unique to your workflow even if you are organizing them by Project.  This will ensure that there is a system-wide organization for the names, and that you can easily filter based on your own work.  A sensible approach might be to have it be something like **\<example-name\>-\<your-initials\>-\<resource-type\>**.  But this is simply a recommendation.  The specific names will be up to you.

## 1. Resource Setup

 In order to use the scripts to create runs, models, pipelines, etc some setup needs to be done.  This section explains the setup that is necessary for any of the example sections.

### Create Project (Optional)
 Jobs execute within a Project.  This section explains how to create a Project.
 
 - This step is only necessary if the Project does not already exist, or if the default Project is not used
   - If the Project exists, use that name when *\<your-project-name\>* is referenced
   - If the default Project is going to be used, then ignore further Project-related actions below
 - Navigate to the `Projects` menu on the far left side of the screen
 - Select `+ Create Project` on the right of the screen
 - Fill in the required fields as follows:
   - **Name:** *`<your-project-name>`* **(your choice of name)**
   - Leave the other fields at their current selection 
 - Submit your Project with the `Submit` button at the bottom of the screen

### Create Code Repo
 A Model is created by running the Training Code on a Dataset.  This section explains how to create a Code repo.  The Dataset is contained within the execution code.
 
  > **Note** In the example, use only lower-case characters in the names that you create. Hyphens are acceptable in any position **other than** the first or last characters, but no other special characters should be used.

 - Navigate to the `Code` menu on the left
 - If an optional Project is being used, choose the Project that you created in the previous step at the top of the screen
   - You only need to do this once.  It will remain the default until changed. <br><br>
 - Select `+ Code`
 - Fill in the required fields as follows:
   - **Name:** *`<your-code-repo>`* **(your choice of name)**
   - **Code Source:** `Git`
   - **URL:** `https://github.com/oneconvergence/dkube-examples.git`
   - **Branch:** `training`
   - Leave the other fields at their current selection 
 - Submit your Code repo with the `Add Code` button at the bottom of the screen

### Create Dataset Repo
 Datasets are used to represent the expected input for model prediction.  The Dataset in this example resides in an S3 bucket.  This section explains how to create a Dataset repo.
 
 - Navigate to the `Datasets` menu on the left
 - Select `+ Dataset`
 - Fill in the required fields as follows:
   - **Name:** *`<your-dataset-repo>`* **(your choice of name)**
   - **Dataset Source:** `Other`
   - **URL:** `https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv`
   - Leave the other fields at their current selection
 - Submit your Dataset repo with the `Add Dataset` button at the bottom of the screen

### Create Model Repo
 An output Model is created as a result of the Training job.  This section explains how to create a Model repo for the output.
 
 - Navigate to the `Models` menu on the left
 - Select `+ Model`
 - Fill in the required fields as follows:
   - **Name:** *`<your-model-repo>`* **(your choice of name)**
   - Leave the other fields at their current selection 
 - Submit your Model repo with the `Add Model` button at the bottom of the screen

### Create JupyterLab IDE
 The first step in the workflow is to experiment with your code, using different datasets and hyperparameters to determine trends.  This section explains how to create a JupyterLab IDE.
 
 - Navigate to the `IDEs` menu on the left
 - Select `+ JupyterLab`
 - Fill in the required fields in the "Basic" tab as follows:
   - **Name:** *`<your-IDE-name>`* **(your choice of name)**
   - **Code:** *`<your-code-repo>`* **(chosen during Code Repo creation)**
   - **Framework:** `tensorflow`
   - **Version:** `2.0.0`
   - Leave the other fields at their current selection 
 - Submit your IDE with the `Submit` button at the bottom of the screen

 > **Note** After the above setup is complete, the other sections can be completed in any order

## 2. Experiment with JupyterLab IDE
 This section explains how to use the JupyterLab IDE to experiment with your Code and hyperparameters.
 
 - Once the IDE is in the `Running` state, select the JupyterLab icon on the far right of the IDE line
   - This will open a JupyterLab tab
 - Navigate to folder <code>/workspace/**\<your-code-repo\>**/insurance</code>
 - Open `training.ipynb`
 - Select `Run All Cells` from the top JupyterLab menu
   - This will execute the file with the current set of inputs
   - The "loss" will be shown at the bottom of the file
 - Change the default NUM_EPOCHS or LEARNING_RATE in the 2nd cell labeled "MACROS"
 - Select `Run All Cells` again
   - This will execute the code again with the new parameter
   - The new "loss" will be shown
 - Make as many changes as you want to see the impact

## 3. Execute Batch Training Jobs
 A Training Job teaches the Model to provide predictions based on the inputs.  This section explains how to create and submit a Training Job.
 
 > **Warning** Do **not** use the `Clone` function from the IDE to create your Run.  That will create a Model with the wrong name.  Follow the instructions below to create your Run.
 
 - Navigate to the `Runs` menu on the left
 - Select `+ Run`, then `Training`
 - Fill in the required fields in the `Basic` tab as follows:
   - **Name:** *`<your-run-name>`* **(your choice of name)**
   - **Code:** *`<your-code-repo>`* **(chosen during Code Repo creation)**
   - **Framework:** `tensorflow`
   - **Framework Version:** `2.0.0`
   - **Start-up command:** `python insurance/training.py`
   - Leave the other fields at their current selection <br><br>
 - Fill in the required fields in the `Repos` tab as follows:
   - **Output** -> **Models:** *`<your-model-repo>`* **(chosen during Model Repo creation)**
 
 > **Warning** The Model Repo needs to be in the `Output` section of the tab.  There is also a Model in the `Input` section, but this is for transfer learning, and should be left blank for this example.
 
 > **Note** Leave the `Mount Path` field blank, since this example does not use that feature.  It uses the MLFlow log model method.

 - Fill in the required fields in the `Configuration` tab as follows:
   - Select the `+` for `Environment variables`
   - Enter variable name "EPOCHS" **(must be upper case)** and value 20
   - Leave the other fields at their current selection 
 - Submit your Run with the `Submit` button at the bottom of the screen <br><br>
 - Create another Run with a different hyperparameter as follows:
   - Select the Run that was created and select `Clone` button
   - Change the "EPOCHS" value in the `Configuration` tab to 15
   - Leave the other fields at their current selection
   - Submit your Run

### Compare Models
 Training Jobs create output Models that can be used to predict output based on new input data.  Each model contains within it the metrics that determine how well the Model is likely to perform.  This section explains how to compare several Model metrics.
 
 - Wait until both Runs from the previous step have completed
 - Navigate to the `Models` menu on the left
 - Expand the Model *\<your-model-repo\>* **(chosen during Model Repo creation)**
 - Select the 2 most recent Model versions (they should be the Models with the highest version numbers)
 - Select `Compare` button
 - Select the `Y-axis` to the left of the graph to `train_loss`
 - The graph will compare the 2 Training Runs

### Submit & Review Katib-Based Hyperparameter Optimization Job
 Katib is used to test a number of different hyperparameters automatically, and choose the best combination based on an output goal.  This section explains how to create and submit a Training Job using Katib.
 
 > **Note** If your OS does not allow you to directly upload the `Tuning File` url specified below, you can select the tuning file by clicking on it.  That will bring up the text in the file.  You can then right-click your mouse and choose `Save as...` to create a tuning file on your local machine.  You can then use that local file to upload the tuning definition.
 
 - Select one of the Runs created in the previous section and select `Clone` button
 - Fill in the required fields in the `Configuration` tab as follows:
   - Select `Upload` button from the `Upload Tuning Definition` section
   - Upload [Tuning File](https://raw.githubusercontent.com/oneconvergence/dkube-examples/training/insurance/tuning.yaml)
     - Right-click on the link above to copy the url address
     - Paste the url address into the dialog box
     > **Note** if the dialog box does not allow you to paste in an address, use the alternate approach as described earlier in this section
   - Leave the other fields at their current selection 
   - Submit your Run <br><br>
 - Wait for the Katib Run to complete
 - Select the Katib icon on the far right of the Run line
   - The Katib Run submits many trial runs with different hyperparameters
   - The graph shows each trial run with the output loss and the input hyperparamters for that trial
   - Scoll down to see which combination was the best, based upon the tuning file

### Deploy Model for Inference Serving
 After the Models have been analyzed and the best one is identified, it is deployed to a server for inference of live data.  This section explains how to deploy a Model.
 
 - Navigate to the `Models` menu on the left
 - Select the Model *\<your-model-repo\>* **(chosen during Model Repo creation)**
 - Choose a Model version
 - Select the `Deploy` icon on the right hand side of the version chosen
 - Fill in the required fields as follows:
   - **Name:** *`<your-deploy-name>`* **(your choice of name)**
   - **Serving Image:** `ocdr/tensorflowserver:2.0.0`
   - **Serving Port:** `8080`
   - **Serving url prefix:** `/v1/models/{MODEL_NAME}`
   - **Deployment:** `Production` radial button
   - **Deploy using:** `CPU` radial button
   - Select `Transformer` checkbox
   - **Transformer Image:** `ocdr/dkube-datascience-tf-cpu:v2.0.0-17`
   - **Transformer Code:** Select *\<your-code-repo\>* **(chosen during Code repo creation)**
   - **Transformer Script:** `insurance/transformer.py`
   - Leave the other fields at their current selection 
 - Submit Deployment using the `Submit` button at the bottom of the screen <br><br>
 - Deployment can be viewed from the `Deployments` menu on the left of the screen
   - Details of the deployment can be viewed by selecting *\<your-deploy-name\>* **(chosen during submission)**
 
 > **Note** Deployments are not filtered by Project

## 4. Create Generic Kubeflow Pipeline
 The workflow can be automated through a Kubeflow Pipeline.  This section explains how to create an example Kubeflow Pipeline.
 
> **Note** This is not an example of the insurance Pipeline.  It is just a general Pipeline to show the concept.
 
 - Create and/or open a JupyterLab instance as described in the section "Create JupyterLab IDE"
 - Navigate to folder <code>/workspace/**\<your-code-repo\>**/pipeline</code>
 - Run all the cells in the file `ControlStructures.ipynb`
 - This will create and run a Kubeflow Pipeline <br><br>
 - Navigate to the `Pipelines` menu on the left
 - Select the `Runs` tab on the top
 - The Pipeline run at the top of the list will be the one that was just created
 - Select the `View Pipeline` field
   - This will show the full Pipeline graph
 - Select the back arrow at the top left and select the Pipeline name
   - This will show the Pipeline as it is executed

## 5. Create Kubeflow Pipeline
 A Kubeflow Pipeline can be created that uses DKube capabilities to integrate the execution and provide a convenient way to analyze the results.  This section explains how to create a Kubeflow Pipeline within DKube for the insurance example.

 > **Note** The follow-on monitor example uses the output of the pipeline execution.  Complete this section before moving on to the monitor example.
 
 - Create and/or open a JupyterLab instance as described in the section "Create JupyterLab IDE"
 - Navigate to folder <code>/workspace/**\<your-code-repo\>**/insurance</code>
 - Open the file `insurance-pipeline.ipynb`
 - Fill in the required fields in the 4th cell as follows:
   - training_program = *\<your-code-repo\>* **(chosen during Code Repo creation)**
   - model = *\<your-model-repo\>* **(chosen during Model Repo creation)**
   - Leave the other fields in their current selection
  - Select `Run All Cells` from the top JupyterLab menu
  - This will create and run a Kubeflow Pipeline for the example <br> <br>
  - Navigate to the `Pipelines` menu on the left
 - Select the `Runs` tab on the top
 - The Pipeline run at the top of the list will be the one that was just created
 - Select the `View Pipeline` field
   - This will show the full Pipeline graph
 - Select the back arrow at the top left and select the Pipeline name
   - This will show the Pipeline as it is executed
   - Select the `dkube-training` graph box to see the Run details
   - Select the `dkube-serving` graph box to see the Deployment details <br><br>
 - Navigate to the `Models` menu on the left
   - Select the `Model` name *\<your-model-repo\>*
   - You will see that the top Model has been deployed

## 6. Inference WebApp
 A model that is running on a production server takes live data and provides an output prediction based on the model training.  A custom application is written to interpret how the model interacts with the live data.  One Convergence has written a web-based inference application for this example.  It is meant to show how this particular example could be used.

 - The WebApp needs to be installed on your local machine
 - In order to install the WebApp, the following command is run once on your machine:
   - `docker run -p 8501:8501 ocdr/streamlit-webapp:insurance-tf`
 - In order to use the WebApp, use the network url that is specified
   - If this does not bring up the WebApp UI, use the following url:
     - http://localhost:8501 <br><br>
 - Fill in the required fields a follows:
   - DKube serving url: `URL of the server running DKube`
     - This is the endpoint url from a running deployment, available from the "Deployments" menu under the "Endpoint" column
   - DKube user auth token: `Authorization token`, available from the Developer Settings menu
   - Select the characteristics of the individual
   - Select `Predict`
