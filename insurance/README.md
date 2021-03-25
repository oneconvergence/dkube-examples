# Insurance Example

## Code
Add Code **insurance**
  - Source: Git
  - URL: https://github.com/oneconvergence/dkube-examples.git
  - Branch : sklearn

## Dataset 
Add dataset **insurance**
  - Source: pub_url
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
  
## Inference webapp
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command  
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance 
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.
