# Insurance Cost Prediction Example
 This example trains a model to predict the cost of insurance based on a set of input characteristics for an individual.  This description provides a step-by-step recipe for running training and using the example.  More details for the platform are available at https://www.dkube.io/guide/guide3_x/Getting_Started.html

## Create Project if it Doesn't Exist
 Jobs execute within a Project.  This section explains how to create a Project.
 
 - Navigate to the Project menu on the far left side of the screen
 - Select "+ Create Project"
 - Name: \<your-project-name\>
 - Leave the other fields in their default options 
 - Submit your Project with the "Add Model" button at the bottom of the screen

## Create Code Repo
 A Model is created by running the Training Code on a Dataset.  This section explains how to create a Code repo.  The Dataset is contained within the execution code.
 
 - Navigate to the Code menu on the left
 - Choose the Project that you created in the previous step at the top of the screen
   - You only need to do this once.  It will remain the default until changed.
 - Select "+ Code"
 - Name: \<your-code-name\>
 - Code Source: Git
 - URL: https://github.com/riteshkarvaloc/dkube-examples.git
 - Branch: training
 - Leave the other fields in their default options 
 - Submit your Code repo with the "Add Code" button at the bottom of the screen

## Create Model Repo
 An output Model is created as as result of the Training job.  This section explains how to create a Model repo for the output.
 
 - Navigate to the Model menu on the left
 - Select "+ Model"
 - Name: \<your-model-repo\>
 - Leave the other fields in their default options 
 - Submit your Model repo with the "Add Model" button at the bottom of the screen

## Experiment with JupyterLab
 The first step in the workflow is to experiment with your code, using different datasets and hyperparameters to determine trends.  This section explains how to create a JupyterLab IDE and experiment with it.
 
 - Navigate to the IDE menu on the left
 - Select Project \<your-project-name\>
 - Select "+ JupyterLab"
 - Within "Basic" tab
   - Name: \<your-IDE\>
   - Code \<your-code-name\>
   - Framework: tensorflow
   - Version: 2.0.0
 - Leave the other fields in their default options 
 - Submit your Code repo with the "Submit" button at the bottom of the screen

## Run training job
 - Selct Project insuracne
 - Runs->+Training Run.
 - Code: insurance
 - Framework: tensorflow
 - Framework Version: 2.0
 - Start-up script: python insurance/training.py
 - Submit

## Katib based Hyperparameter Tuning
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
