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
Run this [pipeline](https://github.com/oneconvergence/dkube-examples/blob/R/mnist/pipeline.R) in RStudio IDE to automate training and serving using kubeflow pipelines.


