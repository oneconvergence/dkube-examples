# Insurance Example

## Code
Add Code **insurance**
  - Source: Git
  - URL: https://github.com/oneconvergence/dkube-examples.git
  - Branch : sklearn

## Dataset 
1. Add dataset **insurance-data**
2. Versioning: None
3. Source s3:
4. Check for AWS
5. Provide your aws key and secret
6. Bucket: mm-workflow
7. Prefix: mm-demo
8. Save

## Model
Add Model **insurance-model**
  - Source: None

## Data scientist workflow

From IDE section launch Jupyter lab with the sklearn framework, with code repo **insurance** and dataset **insurance** with mount point **/opt/dkube/input/**.

  - Open Jupyterlab
  - Go to **workspace/insurance/insurance**
  - Run **insurance.ipynb**

## MLE Workflow

  - For Training/Retraining a model

  - From **workspace/insurance/insurance** run **pipeline.ipynb** to build the pipeline.For retraining specify input_train_type = 'retraining' in the 7th cell.
  - The pipeline includes preprocessing, training and serving stages. 
  - **preprocessing**: the preprocessing stage generates the dataset (either training-data or retraining-data) depending on user choice.
  - **training**: the training stage takes the generated dataset as input, train a sgd model and outputs the model.
  - **serving**: The serving stage takes the generated model and serve it with a predict endpoint for inference. 
  
## Inference webapp
  - Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
  - Run command  
  - > docker run -p 8501:8501 ocdr/streamlit-webapp:insurance 
  - Open http://localhost:8501/ in your browser,
  - Fill serving URL, auth token and other details and click predict.
