# Precomputed Scores Example

- This example supports 3 precomputed dataset sources i.e. **Local, AWS S3 and SQL**. 
- By default this example uses local data source.
  - Local data source is created in DKube storage space
- The notebooks in this example can be run inside or outside Dkube.

## Example Flow
- Create DKube resources. This includes Dataset repo and deployment.
- Create a Modelmonitor. 
- Generate data for analysis by Modelmonitor
  - Precomputed Score data:  Dataset with precomputed scores
- Cleanup resources after the example is complete


## Prerequisites
- For Aws-S3 **(S3 bucket is required)**
  - Create an AWS S3 bucket with the name mm-workflow. 
  - You need access and secret keys to access the bucket.
- For SQL **(SQL database is required)**. 
  - You need the following to access the SQL Database
    - username
    - password
    - hostaddress (server address)
    - portnumber
    - databasename


## Section 1: Create Dkube Resources and Model Monitor

### Launch IDE (Inside Dkube)

#### Note: Follow the instructions if you are running Notebook IDE inside DKube. In case you are Notebook IDE outside DKube then clone the repo and checkout to monitoring branch and follow from step 4 of this section.

1. Add Code. Create Code Repo in Dkube with the following information
  - Name: monitoring-examples
  - Source: Git
  - URL: https://github.com/oneconvergence/dkube-examples.git
  - Branch : monitoring-v3
2. Create an IDE (JupyterLab)
   - Use Tensorflow framework with version 2.0.0
   - **If your data is in local**, move to step 3 directly.
   - **If your data is in aws-s3:**
     - Add the following environment variables with your secret values in configuration tab 
       - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
   - **If your data is in SQL:**
     - Add the following environment variables with your secret values in configuration tab
       - DBUSERNAME
       - DBPASSWORD
       - DBHOSTNAME(should be specified in following format ip:port or domain:port)
       - DATABASENAME    
3. Click Submit.
4. From **workspace/monitoring-examples/precomputed_scores** open modelmonitor.ipynb and fill the following details in the first cell. 
     - **DKUBEUSERNAME** = {your dkube username}
     - **MODELMONITOR_NAME** = {your model monitor name}
     - **PRECOMPUTED_DATA_SOURCE** = { one of your choice in ['local' or 'aws-s3' or 'sql'] }
     - The following will be derived from the environment automatically. Otherwise, please fill in 
       - **TOKEN** = {your dkube authentication token}
       - **DKUBE_URL** = {your dkube url}
       - If the data source is **aws-s3**, fill the below details also:
         - **ACCESS_KEY** = {your s3 access key}
         - **SECRET_KEY** = {your s3 secret key}
       - If the data source is **sql**, fill the below details also:
         - **DBHOSTNAME** = {sql server hostname}
         - **DATABASENAME** = {sql database name} 
         - **DBUSERNAME** = {your username}
         - **DBPASSWORD** = {your password}
         - **DB_PROVIDER** = {provider} (Two values are supported mysql and mssql, default value is mysql)
       - Modelmonitor run frequency in minutes.
         - **RUN_FREQUENCY** = {integer value. units are minutes}
5. Run all the cells. This will create all the dkube resources and model monitor required for this example.
6. After the completion of the notebook, you will see the model monitor `precomputed-mm` in active state.

## Section 2: Data Generation
1. Open [data_generation.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/precomputed_scores/data_generation.ipynb) notebook for generating precomputed scores.
2. Run All Cells. It will start Pushing the data. It uses the data definitions specified in modelmonitor.ipynb file.

## Section 3: SMTP Settings (Optional)
Configure your SMTP server settings on Operator screen. This is optional. If SMTP server is not configured, no email alerts will be generated.

## Section 4: Cleanup
1. After your experiment is complete, 
   - Open [modelmonitor.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/precomputed_scores/modelmonitor.ipynb) and set CLEANUP=True in last Cleanup cell and run.
