# MNIST DIGIT CLASSIFICATION EXAMPLE 

## How to Train the Example in DKube.

## Step1: Create a Code
 1. Click *Repos* side menu option.
 2. Click *+Code* button,
 3. Select Project source as Git.
 4. Enter a unique name say *mnist*
 5. Paste link *[https://github.com/oneconvergence/dkube-examples-2.0/tree/tensorflow/mnist
 ](https://github.com/oneconvergence/dkube-examples-2.0/tree/tensorflow/mnist)* in the URL text box.
 6. Click *Add Code* button.
 7. Code will be created and imported in Dkube. Progress of import can be seen.
 8. Please wait till status turns to *ready*.

## Step2: Create a dataset
 1. Click *Datasets* side menu option.
 2. Click *+Dataset* button.
 3. Select *Others* option.
 4. Enter a unique name say *mnist*
 5. Enter URL as https://s3.amazonaws.com/img-datasets/mnist.pkl.gz.
 6. Click *Add Dataset* button.
 7. Dataset will be created and imported in Dkube. Progress of import can be seen.
 8. Please wait till status turns to *ready*.

## Step3: Create a model
 1. Click *Models* side menu option.
 2. Click *+Model* button.
 3. Enter a unique name say *mnist*.
 4. Select Versioning as DVS. 
 5. Select Model store as default.
 6. Select Model Source as None.
 7. Click the Add Model button.
 8. Model will be created on Dkube.
 9. Please wait till status turns to ready.


## Step4: Start a training job
 1. Click *Runs* side menu option.
 2. Click *+Runs* and select Training button.
 3. Fill the fields in Run form and click *Submit* button. Toggle *Expand All* button to auto expand the form. See below for sample values to be given in the form, for advanced usage please refer to **Dkube User Guide**.
    - **Basic Tab** :
	  - Enter a unique name say *mnist*
 	  - **Container** section
		- Framework - Tensorflow.
    - Framework version - 1.14 or 2.0 depending on your choice
		- Code section - Please select the code *mnist* created in **Step1**.
		- Start-up script -`python train.py`
    - **Repos Tab**
	    - Dataset section - Under Inputs section,select the dataset *mnist* created in **Step2**. Mount point: /mnist .
	    - Model section   - Under Outputs section,select the model *mnist* under Outputs created in **Step3**. Mount point: /opt/dkube/output .
4. Click *Submit* button.
5. A new entry with name *mnist* will be created in *Runs* table.
6. Check the *Status* field for lifecycle of job, wait till it shows *complete*.

## Data Scientist Workflow :
### Steps for running the training program in IDE
1. Create a IDE with tensorflow framework and version 1.6.
2. Select the Code mnist.
3. Under Inputs section, in Repos Tab select dataset Img-DN and enter mount path /mnist.
4. Create a new notebook inside workspace/mnist/mnist
   - In first cell type:
     - %mkdir -p /opt/dkube/output
     - %rm -rf /opt/dkube/output/*
   - In 2nd cell type %load train.py in a notebook cell and then run.
5. Note for running the training more than once, please run the cell 1 again.

### How to Run Notebook
1. Create a IDE with tensorflow framework.
2. Select the Code mnist.
3. Under Inputs section, in Repos Tab select dataset mnist and enter mount path /mnist.
4. Inside the directory workspace/mnist/mnist/, Run all the cells of train.ipynb.

### How to run Pipeline
1. Create Code with name mnist as explained in Step1 above.
2. Create Dataset with name mnist as explained in Step2 above.
3. Create model with name mnist as explained in Step3 above.
4. Download the notebook from https://github.com/oneconvergence/dkube-examples-2.0/blob/tensorflow/mnist/pipeline.ipynb and upload this in default DKube IDE under pipelines folder.
5. Run all the cells of pipeline.ipynb. This will create a pipeline,and  a run.
6. Links are displayed in the output cells wherever applicable.

## Production Workflow
### Test-Inference Details
1. Serving image : (use default one)
2. Transformer image : (use default)
3. Transformer project (use default)
4. Transformer code : program/transformer.py

### How to Test Inference in DKube Webapp
1. Download data sample from https://github.com/oneconvergence/dkube-examples-2.0/blob/tensorflow/mnist/3.png
2. Open the URL https://:32222/inference.
3. Copy the serving endpoint from the test inference tab and paste it into the serving the URL field.
4. Copy token from developer settings and paste into token field.
5. Select model mnist from the dropdown.
6. Upload the downloaded image and click predict.

