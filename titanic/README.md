# Titanic Example from Kaggle

## Create code repo
- Name: sklearn-examples
- Code source: Git
- Git URL: https://github.com/oneconvergence/dkube-examples.git
- Branch: sklearn

## Create dataset repo
- Name: titanic
- Dataset source: Git
- URL: https://github.com/oneconvergence/dkube-examples-internal/tree/master/sklearn/titanic/data


## Create a model
- Name: titanic
- Keep default for others


## Launch Notebook
- Create Jupyterlab IDE with sklearn framework.
- Select the Code sklearn-examples.
- Repos->Inputs->Datasets: select titanic and enter mountpath as /titanic.
- Run workspace/sklearn-examples/titanic/train.ipynb
- You can experiment in the notebook and develop your code. Once you are ready for a formal run, export your code into python script(s)

## Run training job
 - Runs->+Training Run.
 - Code: sklearn-examples
 - Framework: sklearn
 - Version: default (0.23.2)
 - Start-up script: python titanic/train.py
 - Repos->Inputs->Datasets: select titanic and enter mountpath as /titanic
 - Repos->Outputs->Model: select titanic and enter mountpath as /model
 - Submit

## Deploy Model
- Repos->Models->titanic: select a model version
- Deploy
- Name: titanic
- Type: Test
- Transformer: True
- Transformer script: titanic/transformer.py
- Submit

## Test inference
- +tab and go to https://<dkube_url>/inference
- Copy serving endpoint from Deployments->endpoints
- Copy Auth token from Developer settings
- Choose model type as sk-stock
- Upload the test.csv (https://raw.githubusercontent.com/oneconvergence/dkube-examples/sklearn/titanic/test.csv) from repo
- Click predict

## Automate using pipelines
Run this [pipeline](https://github.com/oneconvergence/dkube-examples/blob/sklearn/titanic/pipeline.ipynb) to automate training and serving using kubeflow pipelines.


