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

## Deploy Model (DKube version 2.1.x.x)
- Repos->Models->mnist: select a model version
- Deploy
- Name: mnist
- Type: Test
- Transformer: True
- Transformer script: mnist/transformer.py
- Submit

## Publish and Deploy Model (Dkube version 2.2.x.x)
- Repos->Models->mnist: select a model version
- Click on Publish model icon under ACTIONS column.
- Name: mnist
- Transformer: True
- Transformer script: mnist/transformer.py
- Submit
### Deploy model
- Click on Model catalog and select the published model.
- Click on the deploy model icon under ACTIONS column.
- Enter the deploy model name and select CPU and click Submit.
- Check in Model Serving and wait for the deployed model to change to running state.

## Test inference
- +tab and go to https://<dkube_url>/inference
- Go to test inferences in 2.1.x.x release or model serving in 2.2.x.x and copy the prediction endpoint for the model.
- Copy Auth token from Developer settings
- Choose mnist
- Upload 3.png from repo
- Click predict

## Automate using pipelines
Run this [pipeline](https://github.com/oneconvergence/dkube-examples/blob/pytorch/mnist/pipeline.ipynb) to automate training and serving using kubeflow pipelines.



