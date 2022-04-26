## Sagemaker Insurance Example
This example demonstrates the deployment of model into sagemaker (outside Dkube) and monitoring on Dkube.
## Prerequisites
- **(S3 bucket is required)**. You need access and secret keys to access the bucket.
- Sagemaker access with execution role is required.

### Section 1: Create Dkube Resources
- Add Code. Create Code Repo in Dkube with the following information
  -  Name: monitoring-examples
  -  Source: Git
  -  URL: https://github.com/oneconvergence/dkube-examples.git
  -  Branch : monitoring
- Create an IDE (JupyterLab)
   - In case you are running a Jupyterlab IDE already, you can fill the secret values in [resources.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance_sagemaker/resources.ipynb) and skip the IDE creation.
   - Use sklearn framework
   - Add the following environment variables with your secret values in configuration tab
       - **AWS_ACCESS_KEY_ID**
       - **AWS_SECRET_ACCESS_KEY** 
       - **BUCKET** (Bucket name where the model files and logs will get stored)
       - **ROLE** (AWS IAM Role ARN, eg: `arn:aws:iam::123456789:role/service-role/AmazonSageMaker-ExecutionRole-YYYYMMDDTSSSSS`)
       - **REGION_NAME** (AWS region name, eg: us-east-1)
       - Modelmonitor run frequency in minutes. The same run interval is used for both Drift & Performance monitoring
         - **RUN_FREQUENCY** = {integer value. units are minutes}
   - Click on submit.
   - From **workspace/sagemaker/insurance_sagemaker/**,open and run all the cells of [resources.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance_sagemaker/resources.ipynb). This step will create the resources required.

### Section 2: Deploy the model into sagemaker 
Run all the cells of [sagemaker-insurance.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance_sagemaker/sagemaker-insurance.ipynb). This step will deploy the model in sagemaker and create the endpoint.
### Section 3. Data Generation
Run all the cells of [data_generation.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance_sagemaker/data_generation.ipynb). This step will push the labelled datasets to S3 bucket. By default it pushes data for 60 minutes. For custom, configure minutes variable in the first cell of the notebook.
### Section 4. Model Monitoring
Run all the cells of [modelmonitor.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance_sagemaker/modelmonitor.ipynb).This will create the model monitor in Dkube.
### Section 5: Cleanup
 After your experiment is complete.
- Open sagemaker-insurance.ipynb (and set CLEANUP=True) in the last Cleanup cell and run.
-  Open modelmonitor.ipynb(and set CLEANUP=True) in the last Cleanup cell and run.
-  Open resources.ipynb(and set CLEANUP=True) in last Cleanup cell and run
