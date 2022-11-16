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
