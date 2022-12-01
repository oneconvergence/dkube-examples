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
 - Framework: ~~sklearn~~ tensorflow
 - Version: ~~1.1.1~~ 2.0
 - Start-up script: python insurance/training.py
 - Submit

## Katib based Hyperparameter Tuning
1. Create a Run same as explained above, except that now a tuning file also needs to be uploaded in the configuration tab.
  - For hyperparameter tuning upload the https://github.com/riteshkarvaloc/dkube-examples/blob/training/insurance/tuning.yaml under upload tuning definition. 
  - Submit the run.
