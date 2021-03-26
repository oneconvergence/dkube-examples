# MNIST DIGITS CLASSIFICATION EXAMPLE 

## Create code repo
- Name: pytorch-examples
- Project source: Git
- Git URL: https://github.com/oneconvergence/dkube-examples.git
- Branch: pytorch

## Create dataset repo
- Name: mnist
- Dataset source: Other
- URL: https://s3.amazonaws.com/img-datasets/mnist.pkl.gz


## Create a model
- Name: mnist
- Keep default for others


## Launch Notebook
- Create Jupyterlab IDE with pytorch framework.
- Select the Code pytorch-examples.
- Repos->Inputs->Datasets: select mnist and enter mountpath as /mnist.
- Run workspace/pytorch-examples/mnist/train.ipynb
- You can experient in the notebook and develop your code. Once you are ready for a formal run, export your code into python script(s)

## Run training job
 - Runs->+Training Run.
 - Code: pytorch-examples
 - Framework: pytorch
 - Version: 1.6
 - Start-up script: python mnist/train.py
 - Repos->Inputs->Datasets: select mnist and enter mountpath as /mnist
 - Repos->Outputs->Model: select mnist and enter mountpath as /model
 - Submit

## Deploy Model
- Repos->Models->mnist: select a model version
- Deploy
- Name: mnist
- Type: Test
- Transformer: True
- Transformer script: mnist/transformer.py
- Submit

## Test inference
- +tab and go to https://<dkube_url>/inference
- Copy serving endpoint from Deployments->endpoints
- Copy Auth token from Developer settings
- Choose mnist
- Upload 3.png from repo
- Click predict

## Automate using pipelines
Run this [pipeline](https://github.com/oneconvergence/dkube-examples/blob/pytorch/mnist/pipeline.ipynb) to automate training and serving using kubeflow pipelines.



