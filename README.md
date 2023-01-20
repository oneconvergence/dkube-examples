## Loan Data Accuracy Example

 This example uses Delta Lake to source 2 versions of data that is then used to determine which version is more accurate at determining whether a loan should be provided.  Kafka is used to provide input to the deployed model.

 This example uses one cluster (**Cluster 1**) to train the models, and a different cluster (**Cluster 2**) to serve the model that does the best job.

## Training on Cluster 1

 Cluster 1 is used to train the models and compare their accuracy.

### Create Code Resource

 - Select `Code` repo from left menu

 - Select `+ Code` button and fill in the following fields:

   - **Name:** `deltalake` (**You can choose a different name for this and other resources**)
 
   - **Code Source:** `Git`

   - **URL:** `https://github.com/oneconvergence/dkube-examples/tree/deltalake`

 - Leave the other fields at their current value and `Submit`

### Create Dataset Resource

 - Select `Datasets` from the left menu

 - Select `+ Dataset` button and fill in the following fields:

   - **Name:** `deltalake`

   - **Versioning:** `None`  (**This is not the default**)
 
   - **Dataset Source:** `Deltalake`

   - **Table Source:** `S3`

   - **Table Path:** `dkube-deltalake/loans.delta`

 - Leave the other fields at their current value and `Submit`

### Create Model Resource

 - Select `Models` from the left menu

 - Select `+ Model` button and fill in the following fields:

   - **Name:** `deltalake`

 - Leave the other fields at their current value and `Submit`	

### Create a Jupyterlab IDE

 - Select `IDEs` from the left menu

 - Select `+ JupyterLab` button and fill in the following fields:

   - **Name:**` deltalake`

   - **Framework:** `sklearn`

   - **Framework version:** `0.23.2`  (**This will fill in automatically with the choice of Framework**)

   - **Image:** `ocdr/d3-datascience-sklearn-multiuser:v0.23.2-16`  (**This will fill in automatically with the choice of Framework**)

 - Leave the other fields at their current value and `Submit`

### ML Training inside notebook

 - Launch JupyterLab from the icon at the far right after the IDE is running (this may take several minutes)

 - Navigate to `workspace/deltalake`  (**If you chose a different name than "deltalake" use that name instead**)

#### Train with Version 1 of Data

 - Open `training_version1.ipynb`

 - Click `Run` -> `Run All Cells`

#### Train with Version 2 of Data

 - Open `training_version2.ipynb`

 - Click `Run` > `Run All Cells`

### ML Training with Version 1 of Data as Standalone Run

 - Select `Runs` from left menu

 - Select `+ Run` > `Training Run` & fill in the following fields:

   - `Basic` Tab
 
     - **Name:** `deltalake`

     - **Code:** `deltalake`  (**If you chose a different name for your code, use it here instead**)

     - **Framework:** `sklearn`  (**The correct version and image will be filled in**)

     - **Startup Command:** `python training_version1.py`

   - `Repos` Tab

     - **Inputs** `+ Dataset`

       - Choose `deltalake`  (**Or the name that you chose for your Dataset**)

       - **Version:** 1  (**It will default to version 2, so you must change it**)

       - **Mountpath:** `/mnt/deltalake`

     - **Outputs ** `+ Model`

       - Choose `deltalake`  (**Or the name that you chose for your Model**)

       - **Mountpath:** `/mnt/model`

    > **Note** There is a `Model` section in the Inputs.  Make sure that you enter the Model in the **Output** section only
 
 - Leave the other fields at their current value and `Submit`

### ML Training with Version 2 of Data as Standalone Run

 - Select `Runs` from left menu

 - Select `+ Run` > `Training Run` & fill in the following fields:

   - `Basic` Tab
 
     - **Name:** `deltalake`

     - **Code:** `deltalake`  (**If you chose a different name for your code, use it here instead**)

     - **Framework:** `sklearn`  (**The correct version and image will be filled in**)

     - **Startup Command:** `python training_version2.py`

     > **Note** If you use `Clone` to create the 2nd Run, make sure that you change the startup command to Version 2

   - `Repos` Tab

     - **Inputs** `+ Dataset`

       - Choose `deltalake`  (**Or the name that you chose for your Dataset**)

       - **Version:** 2  (**If you use `Clone` to create the 2nd Run, make sure that you change this**)

       - **Mountpath:** `/mnt/deltalake`

     - **Outputs** `+ Model`

       - Choose `deltalake`  (**Or the name that you chose for your Model**)

       - **Mountpath:** `/mnt/model`

    > **Note** There is a `Model` section in the Inputs.  Make sure that you enter the Model in the **Output** section only
 
 - Leave the other fields at their current value and `Submit` - Select `Runs` from left menu

### Compare the Runs for Accuracy

- Wait for Runs to `complete`

- Select the 2 runs and `Compare`

- Choose the run with best accuracy and proceed with below steps to deploy the model

- Click `Run` > `Lineage` > `Output Models` 

- Click the model version

- Click `Build Image`

  - Defaults are auto filled

- Click `Submit` button

- Wait for the image build to be successful

- Click `Model` > `Details` > `Images` > `Image Name`

- Copy the value in `Image` field

## Serving on Cluster 2

 Move from **Cluster 1** to **Cluster 2** in order to complete the deployment.
 
 - Select `Deployments` from left menu
 
 - Select `+ Deployment` button and fill in the fields as follows:

   - Paste the Image built in above setup

	Click "EventSource" and choose "Kafka" and enter below values

		Brokers : dkube-kafka-cp-kafka.dkube-kafka:9092

		Topics : <username>

		Consumer group : training

	Wait for "Deployment" to get to "Running" state


## Test Inference
Webapp will be available @ dkubeserving-clusterip:31333
	
Input the below values,
	
	Kafka broker endpoint : dkube-kafka-cp-kafka-headless.dkube-kafka:9092
	
	Kafka topic : <username>
	
	Select Version : version2
	
	Number of times to send : 1
	
Click "Predict" button
