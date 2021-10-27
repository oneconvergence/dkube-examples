# INSURANCE EXAMPLE

- This example supports 3 dataset sources i.e. **Local, Aws_S3 and SQL**. 
- By default this example uses local data source.
- The notebooks in this example can be run inside or outside Dkube.

## Example Flow
- **Insurance model training** 
  - Follow this README only.
- **Model monitoring using UI**
  - Follow this README (Dkube Resources step) and then jump to [README.ui.md](https://github.com/oneconvergence/dkube-examples/blob/monitoring/insurance/README.ui.md) for the next steps.
- **Model monitoring using SDK**
  - Follow this README (Dkube Resources step) and then jump to [README.sdk.md](https://github.com/oneconvergence/dkube-examples/blob/monitoring/insurance/README.sdk.md) for the next steps.

## Prerequisites
- For Aws_S3 **(S3 bucket is required)**
  - Create an AWS S3 bucket with the name mm-workflow. You need access and secret key to access the bucket.
- For SQL **(SQL database is required)**. You need username,password,hostaddress,portnumber,databasename to access the SQL database.


## Dkube Resources
#### Note: Skip the Dataset (SQL) step if your data is in aws-s3 or in local.It will be automatically created by resources.ipynb notebook.

### Dataset (SQL)
1. Add dataset **insurance-data-sql**
2. Versioning: None
3. Source : SQL
4. Provider : MYSQL
5. Select password and fill the details
- Username, Password, HostAddress, PortNumber, Database Name

### Launch IDE (Inside Dkube)
1. Create an IDE (JupyterLab)
   - Use sklearn framework
2. **If your data is in local**, move to step 3 directly.
  - **If your data is in aws_s3:**
     - Add these [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY] environment variables with your secret values in configuration tab 
  - **If your data is in SQL:**
     - Add these [USERNAME, PASSWORD, HOSTADDRESS,DATABASENAME] environment variables with your secret values in configuration tab    
3. Click Submit.
4. Download [resources.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/resources.ipynb) and upload the notebook and fill the details in the first cell.
     - **MODELMONITOR_NAME** = {your model monitor name}
     - **DATASET_SOURCE** = { one of your choice in ['local' or 'aws_s3' or 'sql'] }
     - **INPUT_TRAIN_TYPE** = {'training'}
5. Run all the cells. This will create all the dkube resources required for this example automatically. It will also create a details.txt file which contains the model monitor information.

### Outside Dkube:
1. Open resources.ipynb and fill the details in first cell.
     - **MODELMONITOR_NAME** = {your model monitor name}
     - **DATASET_SOURCE** = { one of your choice in ['local' or 'aws_s3' or 'sql'] }
     - **INPUT_TRAIN_TYPE** = {'training'}
     - **OUTSIDE_DKUBE** = True
     - **TOKEN** = {your dkube authentication token}
     - **URL** = {your dkube url}
     - **DKUBEUSERNAME** = {your dkube username}
2. If the data source is **aws_s3**, fill the below details also:
     - **ACCESS_KEY** = {your s3 access key}
     - **SECRET_KEY** = {your s3 secret key}
3. If the data source is **sql**, fill the below details also:
     - **HOSTNAME** = {sql server hostname}
     - **DATABASENAME** = {sql database name} 
     - **DBUSERNAME** = {your username}
     - **PASSWORD** = {your password}
4. Run all the cells.

## Insurance Model Training
1. From **workspace/insurance/insurance** open **train.ipynb** to build the pipeline.
2. The pipeline includes preprocessing, training and serving stages. Run all cells
     - **preprocessing**: the preprocessing stage generates the dataset (either training-data or retraining-data) depending on user choice.
     - **training**: the training stage takes the generated dataset as input, train a sgd model and outputs the model.
     - **serving**: The serving stage takes the generated model and serve it with a predict endpoint for inference. 
3. Verify that the pipeline has created the following resources
     - Datasets: 'insurance-training-data' with version v2.
     - Model: 'insurance-model' with version v2

### Inference
1. Go to webapp directory, and build a docker image with given **Dockerfile** or pull **ocdr/streamlit-webapp:insurance**.
2. Run command  
     - docker run -p 8501:8501 ocdr/streamlit-webapp:insurance 
3. Open http://localhost:8501/ in your browser,
     - Fill serving URL, auth token and other details and click predict.
