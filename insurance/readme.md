# Insurance Cost Prediction Example
 This example trains a model to predict the cost of insurance based on a set of input characteristics for an individual.  This description provides a step-by-step recipe for running training and using the example.  More details for the platform are available at https://www.dkube.io/guide/guide3_x/Getting_Started.html

## Create Project if it Doesn't Exist
 Jobs execute within a Project.  This section explains how to create a Project.
 
 - Navigate to the "Project" menu on the far left side of the screen
 - Select "+ Create Project"
 - Fill in the required fields as follows:
   - Name: \<your-project-name\> (your choice of name)
   - Leave the other fields in their default selection 
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
   - URL: https://github.com/riteshkarvaloc/dkube-examples.git
   - Branch: training
   - Leave the other fields in their default selection 
 - Submit your Code repo with the "Add Code" button at the bottom of the screen

## Create Model Repo
 An output Model is created as as result of the Training job.  This section explains how to create a Model repo for the output.
 
 - Navigate to the "Model" menu on the left
 - Select "+ Model"
 - Fill in the required fields as follows:
   - Name: \<your-model-repo\> (your choice of name)
   - Leave the other fields in their default selection 
 - Submit your Model repo with the "Add Model" button at the bottom of the screen

## Create a JupyterLab IDE
 The first step in the workflow is to experiment with your code, using different datasets and hyperparameters to determine trends.  This section explains how to create a JupyterLab IDE.
 
 - Navigate to the "IDE" menu on the left
 - Select Project \<your-project-name\> (chosen in previous step)
 - Select "+ JupyterLab"
 - Fill in the required fields in the "Basic" tab as follows:
   - Name: \<your-IDE-name\> (your choice of name)
   - Code \<your-code-repo\> (chosen during Code Repo creation)
   - Framework: tensorflow
   - Version: 2.0.0
   - Leave the other fields in their default selection 
 - Submit your IDE with the "Submit" button at the bottom of the screen

## Experiment with the JupyterLab IDE
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
 - Select Project \<your-project-name\> (chosen during Project creation)
 - Select "+ Run", then "Training"
 - Fill in the following fields in the "Basic" tab as follows:
   - Name: \<your-run-name\> (your choice of name)
   - Code: \<your-code-repo\> (chosen during Code Repo creation)
   - Framework: tensorflow
   - Framework Version: 2.0.0
   - Start-up command: python insurance/training.py
   - Leave the other fields in their default selection <br><br>
 - Fill in the following fields in the "Repos" tab as follows:
   - Output -> Models: \<your-model-repo\> (chosen during Model Repo creation) <br><br>
 - Fill in the following fields in the "Configuration" tab as follows:
   - Select the "+" for "Environment variables"
   - Enter variable name "EPOCHS" (must be upper case) and value 20
   - Leave the other fields in their default selection 
 - Submit your Run with the "Submit" button at the bottom of the screen <br><br>
 - Create another Run with a different hyperparameter as follows:
   - Select the Run that was created and select "Clone" button
   - Change the "EPOCHS" value in the "Configuration" tab to 15
   - Leave the other fields in their default selection
   - Submit your Run

## Compare Models
 Training Jobs create output Models that can be used to predict output based on new input data.  Each model contains within it the metrics that determine how well the Model is likely to perform.  This section explains how to compare several Model metrics.

## Katib-Based Hyperparameter Tuning
 Katib is used to test a number of different hyperparameters automatically, and choose the best combination based on an output goal.  This section explains how to create and submit a Training Job using Katib.
 
1. Create a Run same as explained above, except that now a tuning file also needs to be uploaded in the configuration tab.
  - For hyperparameter tuning upload the https://github.com/riteshkarvaloc/dkube-examples/blob/training/insurance/tuning.yaml under upload tuning definition. 
  - Submit the run.

## Deployment:
 - Click on run and go to model lineage.
 - Click on the model in outputs.
 - Click on deploy
 - Give a name and use serving image `ocdr/tensorflowserver:2.0.0`
 - Choose deployment type `Test` and deploying using `CPU`
 - Select transformer
 - Use transformer image `ocdr/dkube-datascience-tf-cpu:v2.0.0-16`
 - Select transformer code `insurance`
 - transformer script `insurance/transformer.py`
 - Submit. 

## Pipeline
 - Once the code repo is added, create an IDE and launch
 - From `workspace/insurance/insurance` open `insurance_pipeline.ipynb`
 - Verify the inputs in 4th cell
 - Run all the cells

## Inference webapp
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance-tf
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.
