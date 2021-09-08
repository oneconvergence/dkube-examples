# Insurance Example

## Code
Add Code **insurance**
  - Source: Git
  - URL: https://github.com/oneconvergence/dkube-examples.git
  - Branch : sklearn

## Dataset 
Add dataset **insurance**
  - Source: other
  - URL: https://storage.googleapis.com/insurance-data/insurance/insurance.csv

## Model
Add Model **insurance**
  - Source: None

## Featureset
Add featuresret **insurance-fs**
  - Spec upload: None


## Data scientist workflow

From IDE section launch Jupyter lab with the sklearn framework, with code repo **insurance** and dataset **insurance** with mount point **/opt/dkube/input/**.

  - Open Jupyterlab
  - Go to **workspace/insurance/insurance**
  - Run **insurance.ipynb**

## MLE Workflow

  - From **workspace/insurance/insurance** run **pipeline.ipynb** to build the pipeline, the pipeline includes preprocessing, training and serving stages. 
  - **preprocessing**: the preproceessing state takes insurance data as input, and after the feature engineering on data it generates a feetureset. 
  - **training**: the training stage takes the generated featureset as input, train a linear regression model and outputs the model.
  - **serving**: The serving stage takes the generated model and serve it with a predict endpoint for inference. 
  
## Run preprocessing job
 - Runs->+preprocessing Run.
 - Code: dkube-examples
 - Framework: Custom
 - Image: docker.io/ocdr/d3-datascience-sklearn:v0.23.2
 - Start-up script: python insurance/preprocessing.py --fs insurance-fs
 - Repos->Inputs->Datasets: select dataset and enter mountpath as /opt/dkube/in
 - Repos->Outputs->featureset: select featureset and enter mountpath as /opt/dkube/out
 - Submit
 
## Run training job
 - Runs->+training Run.
 - Code: dkube-examples
 - Framework: Sklearn
 - Version: 0.23.2
 - Start-up script: python insurance/training.py --fs insurance-fs
 - Repos->Inputs->featureset: select featureset and enter mountpath as /opt/dkube/in
 - Repos->Outputs->model: select model and enter mountpath as /opt/dkube/out
 - Submit
 
## Deploy Model (DKube version 2.1.x.x)
- Repos->Models->insurance: select a model version
- Deploy
- Name: insurance
- Type: Test
- Transformer: True
- Transformer script: insurance/transformer.py
- Submit

## Publish and Deploy Model (Dkube version 2.2.x.x)
- Repos->Models->insurance: select a model version
- Click on Publish model icon under ACTIONS column.
- Name: insurance
- Transformer: True
- Transformer script: insurance/transformer.py
- Submit

### Deploy model
- Click on Model catalog and select the published model.
- Click on the deploy model icon under ACTIONS column.
- Enter the deploy model name and select CPU and click Submit.
- Check in Model Serving and wait for the deployed model to change to running state.
  
## Inference webapp
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command  
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance 
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.
