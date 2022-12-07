# Insurance Cost Prediction Example
 This example trains a model to predict the cost of insurance based on a set of input characteristics for an individual.  This description provides a step-by-step recipe for using the example.  More details for the platform are available at https://www.dkube.io/guide/guide3_x/Getting_Started.html <br><br>
 This example contains the following capabilities:
 
 - Create the Repos required for training
 - Create and experiment with a JupyterLab IDE
 - Create and run Training Jobs and compare their output metrics
 - Submit and review a Katib-based Hyperparameter optimization job
 - Deploy a Model for inference serving
 - Create a Kubeflow Pipeline

## Create Project
 Jobs execute within a Project.  This section explains how to create a Project.
 
 - This step is only necessary if the Project does not already exist, or if the default Project is not used
   - If the Project exists, use that name when \<your-project-name\> is referenced
   - If the default Project is going to be used, then ignore further Project-related actions below
 - Navigate to the "Project" menu on the far left side of the screen
 - Select "+ Create Project" on the right of the screen
 - Fill in the required fields as follows:
   - Name: \<your-project-name\> (your choice of name)
   - Leave the other fields at their current selection 
 - Submit your Project with the "Submit" button at the bottom of the screen

## Create Code Repo
 A Model is created by running the Training Code on a Dataset.  This section explains how to create a Code repo.  The Dataset is contained within the execution code.
 
 - Navigate to the "Code" menu on the left
 - Choose the Project that you created in the previous step at the top of the screen
   - You only need to do this once.  It will remain the default until changed.
 - Select "+ Code"
 - Fill in the required fields as follows:
   - Name: \<your-code-repo\> (your choice of name)
   - Code Source: Git
   - URL: https://github.com/oneconvergence/dkube-examples.git
   - Branch: training
   - Leave the other fields at their current selection 
 - Submit your Code repo with the "Add Code" button at the bottom of the screen

## Create Model Repo
 An output Model is created as as result of the Training job.  This section explains how to create a Model repo for the output.
 
 - Navigate to the "Models" menu on the left
 - Select "+ Model"
 - Fill in the required fields as follows:
   - Name: \<your-model-repo\> (your choice of name)
   - Leave the other fields at their current selection 
 - Submit your Model repo with the "Add Model" button at the bottom of the screen

## Create JupyterLab IDE
 The first step in the workflow is to experiment with your code, using different datasets and hyperparameters to determine trends.  This section explains how to create a JupyterLab IDE.
 
 - Navigate to the "IDEs" menu on the left
 - Ensure that Project \<your-project-name\> is selected (chosen when creating Project)
 - Select "+ JupyterLab"
 - Fill in the required fields in the "Basic" tab as follows:
   - Name: \<your-IDE-name\> (your choice of name)
   - Code \<your-code-repo\> (chosen during Code Repo creation)
   - Framework: tensorflow
   - Version: 2.0.0
   - Leave the other fields at their current selection 
 - Submit your IDE with the "Submit" button at the bottom of the screen

## Experiment with JupyterLab IDE
 This section explains how to use the JupyterLab IDE to experiment with your Code and hyperparameters.
 
 - Once the IDE is in the "Running" state, select the JupyterLab icon on the far right of the IDE line
   - This will create a JupyterLab tab
 - Navigate to /workspace/\<your-code-repo\>/insurance
 - Open training.ipynb
 - Select "Run All Cells" from the top JupyterLab menu
   - This will execute the file with the current set of inputs
   - The "loss" will be shown at the bottom of the file
 - Change the default NUM_EPOCHS within the MACROS section to "15"
 - Select "Run All Cells" again
   - This will execute the code again with the new parameter
   - The new "loss" will be shown
 - Make as many changes as you want to see the impact

## Run Training Jobs
 A Training Job teaches the Model to provide predictions based on the inputs.  This section explains how to create and submit a Training Job.
 
 - Navigate to the "Runs" menu on the left
 - Ensure that Project \<your-project-name\> is selected (chosen when creating Project)
 - Select "+ Run", then "Training"
 - Fill in the required fields in the "Basic" tab as follows:
   - Name: \<your-run-name\> (your choice of name)
   - Code: \<your-code-repo\> (chosen during Code Repo creation)
   - Framework: tensorflow
   - Framework Version: 2.0.0
   - Start-up command: python insurance/training.py
   - Leave the other fields at their current selection <br><br>
 - Fill in the required fields in the "Repos" tab as follows:
   - Output -> Models: \<your-model-repo\> (chosen during Model Repo creation) <br><br>
 - Fill in the required fields in the "Configuration" tab as follows:
   - Select the "+" for "Environment variables"
   - Enter variable name "EPOCHS" (must be upper case) and value 20
   - Leave the other fields at their current selection 
 - Submit your Run with the "Submit" button at the bottom of the screen <br><br>
 - Create another Run with a different hyperparameter as follows:
   - Select the Run that was created and select "Clone" button
   - Change the "EPOCHS" value in the "Configuration" tab to 15
   - Leave the other fields at their current selection
   - Submit your Run

## Compare Models
 Training Jobs create output Models that can be used to predict output based on new input data.  Each model contains within it the metrics that determine how well the Model is likely to perform.  This section explains how to compare several Model metrics.
 
 - Wait until both Runs from the previous step have completed
 - Navigate to the "Models" menu on the left
 - Expand the Model \<your-model-repo\> (chosen during Model Repo creation)
 - Select the 2 most recent Model versions (they should be the Models with the highest version numbers)
 - Select "Compare" button
 - Select the "Y-axis" to the left of the graph to "train_loss" 
 - The graph will compare the 2 Training Runs

## Submit & Review Katib-Based Hyperparameter Optimization Job
 Katib is used to test a number of different hyperparameters automatically, and choose the best combination based on an output goal.  This section explains how to create and submit a Training Job using Katib.
 
 - Download the hyperparameter optimization file https://oneconvergence.com/guide2/downloads/insurance-tuning.yaml
 - Select one of the Runs created in the previous section and select "Clone" button
 - Fill in the required fields in the "Configuration" tab as follows:
   - Select "Upload" button from the "Upload Tuning Definition" section
   - Choose the tuning file that was downloaded previously
   - Leave the other fields at their current selection 
   - Submit your Run <br><br>
 - Wait for the Katib Run to complete
 - Select the Katib icon on the far right of the Run line
   - The Katib Run submits many trial runs with different hyperparameters
   - The graph shows each trial run with the output loss and the input hyperparamters for that trial
   - Scoll down to see which combination was the best, based upon the tuning file

## Deploy Model for Inference Serving
 After the Models have been analyzed and the best one is identified, it is deployed to a production server for inference of live data.  This section explains how to deploy a Model.
 
 - Navigate to the "Models" menu on the left
 - Ensure that Project \<your-project-name\> is selected (chosen when creating Project)
 - Select the Model \<your-model-repo\> (chosen during Model Repo creation)
 - Choose a Model version
 - Select the "Deploy" icon on the right hand side of the version chosen
 - Fill in the required fields as follows:
   - Name: \<your-deploy-name\> (your choice of name)
   - Serving Image: ocdr/tensorflowserver:2.0.0
   - Deployment: "Test" radial button
   - Deploy using: "CPU" radial button
   - Select "Transformer" checkbox
   - Transformer Image: ocdr/dkube-datascience-tf-cpu:v2.0.0-16
   - Transfomer code: \<your-code-repo\>
   - Transformer Script: insurance/transformer.py
   - Leave the other fields at their current selection 
 - Submit Deployment using the "Submit" button at the bottom of the screen <br><br>
 - Deployment can be viewed from the "Deployments" menu on the left of the screen
   - Details of the deployment can be viewed by selecting \<your-deploy-name\> (chosen during submission)

## Create Kubeflow Pipeline
 The workflow can be automated through a Kubeflow Pipeline.  This section explains how to create a pipeline.
 
 - A pipeline is created from a JupyterLab IDE
 - Launch or select the JupyterLab IDE \<your-IDE-name\> (created in the IDE section)
 - Navigate to folder "workspace/\<your-code-repo\>/insurance"
 - Open file "insurance_pipeline.ipynb"
 - Review the 4th cell and ensure that the inputs are as follows:
   - image = "ocdr/dkube-datascience-tf-cpu:v2.0.0-16"
   - serving_image = "ocdr/tensorflowserver:2.0.0"
   - training_program = "training"
   - model = 'insurance'
   - training_script = "python insurance/training.py"
   - transformer_code='insurance/transformer.py'
   - framework = "tensorflow"
   - f_version = "2.0.0"
   - output_mount_point = "/opt/dkube/out"
 - Select "Run All Cells" from the top JupyterLab menu

<!--- ## Inference webapp
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance-tf
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.
-->
