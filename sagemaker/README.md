## Sagemaker Insurance Example
This example demonstrates the deployment of model into sagemaker (outside Dkube) and monitoring on Dkube.
## Prerequisites
- **(S3 bucket is required)**. You need access and secret keys to access the bucket.
- Sagemaker access is required.

### Section 1: Create Dkube Resources
Add Code. Create Code Repo in Dkube with the following information
  -  Name: sagemaker
  -  Source: Git
  -  URL: https://github.com/oneconvergence/dkube-examples.git
  -  Branch : monitoring
- Create an IDE (JupyterLab)
   - Use sklearn framework
   - Add the following environment variables with your secret values in configuration tab
       - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET, ROLE, REGION_NAME
   - Click on submit.
   - From **workspace/sagemaker/sagemaker/**,open and run all the cells of **resources.ipynb**. This step will create the resources required.

### Section 2: Deploy the model into sagemaker 
Run all the cells of sagemaker-insurance.ipynb. This step will deploy the model in sagemaker and create the endpoint.
### Section 3. Data Generation
Run all the cells of data_generation.ipynb. This step will push the labelled datasets to S3 bucket.
### Section 4. Model Monitoring
Run all the cells of modelmonitor.ipynb.This will create the model monitor in Dkube.
### Section 5: Cleanup
 After your experiment is complete.
-  Open resources.ipynb(and set CLEANUP=True) in last Cleanup cell and run
-  Open modelmonitor.ipynb(and set CLEANUP=True) in the last Cleanup cell and run.

