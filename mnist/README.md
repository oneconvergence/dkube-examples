# MNIST DIGITS CLASSIFICATION EXAMPLE 

## Create code repo
- Name: r-examples
- Project source: Git
- Git URL: https://github.com/oneconvergence/dkube-examples.git
- Branch: R

## Create dataset repo
- Name: mnist
- Dataset source: Other
- URL: https://s3.amazonaws.com/img-datasets/mnist.pkl.gz


## Create a model
- Name: mnist
- Keep default for others


## Run training job
 - Runs->+Training Run.
 - Code: r-examples
 - Framework: Tensorflow
 - Version: r-2.0.0
 - Start-up script: r mnist/train.R
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

## Publish and Deploy Model (Dkube version 3.0.x.x)
- Models->mnist: select a model version
- Click on Publish model icon under ACTIONS column
- Transformer: True
- Transformer script: mnist/transformer.py
- Submit
### Deploy model
- Click on Models in the navigation pane
- Click on the drop down next to 'Owned by me' and select 'Published'
- Click on the published model 'mnist'
- Select the published version and click on the deploy model icon under ACTIONS column
- Enter the deploy model name, select Deployment / Test and select Deploy using / CPU. Click Submit
- Check in Deployments and wait for the deployed model to change to running state

## Test inference
- Go to
  - Deployments in 2.1.x.x version
  - Model Serving in 2.2.x.x version
  - Deployments in 3.0.x.x version
- Copy the prediction Endpoint for the model
- Create a browser tab and go to https://<dkube_url>/inference
- Paste the Endpoint URL
- Copy Auth token from Developer settings in Dkube page and Paste in inference page
- Choose mnist
- Upload 3.png from repo
- Click predict

## Automate using pipelines
Run this [pipeline](https://github.com/oneconvergence/dkube-examples/blob/R/mnist/pipeline.R) in RStudio IDE to automate training and serving using kubeflow pipelines.


