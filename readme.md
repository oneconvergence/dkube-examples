# Insurance cost prediction EXAMPLE 

## Create code repo
- Name: insurance
- Project source: Git
- Git URL: https://github.com/riteshkarvaloc/dkube-examples.git
- Branch: training


## Create a model
- Name: insurance
- Keep default for others


## Run training job
 - Runs->+Training Run.
 - Code: insurance
 - Framework: sklearn
 - Version: 1.1.1
 - Start-up script: python insurance/train-hyp.py
 - Repos->Outputs->Model: select insurance and enter mountpath as /model
 - Submit

## Katib based Hyperparameter Tuning
1. Create a Run same as explained above, except that now a tuning file also needs to be uploaded in the configuration tab.
  - For hyperparameter tuning upload the https://github.com/riteshkarvaloc/dkube-examples/blob/training/insurance/tuning.yaml under upload tuning definition. 
  - Submit the run.
