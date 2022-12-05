# Insurance cost prediction EXAMPLE 

## Create Project if doesn't exist
 - Name: insurance

## Create code repo
 - Name: insurance
 - Project source: Git
 - Git URL: https://github.com/riteshkarvaloc/dkube-examples.git
 - Branch: training

## Run training job
 - Selct Project insuracne
 - Runs->+Training Run.
 - Code: insurance
 - Framework: tensorflow
 - Version: 2.0
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


## Inference webapp
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance-tf
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.