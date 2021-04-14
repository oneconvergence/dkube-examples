# MNIST DIGITS CLASSIFICATION EXAMPLE 

## Create code repo
- Name: dkube-examples
- Project source: Git
- Git URL: https://github.com/oneconvergence/dkube-examples.git
- Branch: tensorflow

## Create dataset repo
- Name: mnist
- Dataset source: Other
- URL: https://s3.amazonaws.com/img-datasets/mnist.pkl.gz


## Create a model
- Name: mnist
- Keep default for others


## Launch Notebook
- Create Jupyterlab IDE with tensorflow framework.
- Select the Code mnist.
- Repos->Inputs->Datasets: select mnist and enter mountpath as /mnist.
- Run workspace/dkube-examples/mnist/train.ipynb
- You can experient in the notebook and develop your code. Once you are ready for a formal run, export your code into python script(s)

## Run training job
 - Runs->+Training Run.
 - Code: dkube-examples
 - Framework: Tensorflow
 - Version: 2.0.0
 - Start-up script: python mnist/train.py
 - Repos->Inputs->Datasets: select mnist and enter mountpath as /mnist
 - Repos->Outputs->Model: select mnist and enter mountpath as /model
 - Submit

## Katib based Hyperparameter Tuning
1. Create a Run same as explained above, except that now a tuning file also needs to be uploaded in the configuration tab.
  - For hyperparameter tuning upload the https://github.com/oneconvergence/dkube-examples/blob/tensorflow/mnist/tuning.yaml under upload tuning definition. 
  - Submit the run. 

## Tuning.yaml file Details:
1. **objective**: The metric that you want to optimize. 
2. **goal** parameter is mandatory in tuning.yaml file.
3. **objectiveMetricName:** Katib uses the objectiveMetricName and additionalMetricNames to monitor how the hyperparameters work with the model. Katib records the value of the best objectiveMetricName metric.
4. **parameters : **The range of the hyperparameters or other parameters that you want to tune for your machine learning (ML) model.
5. **parallelTrialCount**: The maximum number of hyperparameter sets that Katib should train in parallel. The default value is 3.
6. **maxTrialCount**: The maximum number of trials to run.
7. **maxFailedTrialCount**: The maximum number of failed trials before Katib should stop the experiment.
8. **algorithm**: The search algorithm that you want Katib to use to find the best hyperparameters or neural architecture configuration. 

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
- 
## Test inference
- +tab and go to https://<dkube_url>/inference
- Go to test inferences in 2.1.x.x release or model serving in 2.2.x.x and copy the prediction endpoint for the model.
- Copy Auth token from Developer settings
- Choose mnist
- Upload 3.png from repo
- Click predict

## Automate using pipelines
Run this [pipeline](https://github.com/oneconvergence/dkube-examples/blob/tensorflow/mnist/pipeline.ipynb) to automate training and serving using kubeflow pipelines.


