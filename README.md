# Download loan data and put loan.csv in the root folder

# Notebooks workflow
1. Run load_deltalake.ipynb
This notebook will create delta lake table and create two versions of table with different features of the loan data

2. Run training_version1.ipynb
This notebook runs with version=1 of the delta lake table.
Note the accuracy.

3. Run training_version2.iynb
This notebook runs with version=2 of the delta lake table.
Note that accuracy is better than in step 2.

# Training
Use the training.py with the Dkube training job.

# Training with delta lake table in S3
AWS credentials should be available in standard way either as env vars or ~/.aws/credentials
Use the s3_training.py with DKube training job.
It creates a delta lake table in S3, loads versions in it and performs training with the version of data in deltalake.
