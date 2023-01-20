## Loan Data Accuracy Example

This example uses Delta Lake to source 2 versions of data that is then used to determine which version is more accurate at determining whether a loan should be provided.  Kafka is used to provide input to the deployed model.

This example uses one cluster (**Cluster 1**) to train the models, and a different cluster (**Cluster 2**) to serve the model that does the best job.

## Training on Cluster 1

Cluster 1 is used to train the models and compare their accuracy.

### Create Code Resource

Select `Code` repo from left menu

Select `+ Code` button and fill in the following fields:

 - **Name:** `deltalake` (**You can choose a different name for this and other resources, in which case you would use that name throughout this example**)
 
 - **Code Source:** `Git`

 - **URL:** `https://github.com/oneconvergence/dkube-examples/tree/deltalake`

 - Leave the other fields at their current value and `Submit`

### Create Dataset Resource

Select `Datasets` from the left menu

Select `+ Dataset` button and fill in the following fields:

 - **Name:** `deltalake`

 = **Versioning:** `None`  (**This is not the default**)
 
 - **Dataset Source:** `Deltalake`

 - **Table Source:** `S3`

 - **Table Path:** `dkube-deltalake/loans.delta`

 - Leave the other fields at their current value and `Submit`

### Create Model Resource

Select `Models` from the left menu

Select `+ Model` button and fill in the following fields:

 - **Name:** `deltalake`

 - Leave the other fields at their current value and `Submit`	

### Create a Jupyterlab IDE

Select `IDEs` from the left menu

Select `+ JupyterLab` button and fill in the following fields:

 - **Name:**` deltalake`

 - **Framework:** `sklearn`

 - **Framework version:** `0.23.2`  (**This will fill in automatically with the choice of Framework**)

 - **Image:** `ocdr/d3-datascience-sklearn-multiuser:v0.23.2-16`  (**This will fill in automatically with the choice of Framework**)

 - Leave the other fields at their current value and `Submit`

### ML Training inside notebook

Launch JupyterLab from the icon at the far right after the IDE is running (this may take several minutes)

Navigate to `workspace/deltalake`  (**If you chose a different name than "deltalake" use that name instead**)

#### Train with version 1 of data
	Open "training_version1.ipynb"

	Click Run : Run All Cells

###### Train with version 2 of data
	Open "training_version2.ipynb"

	Click Run : Run All Cells

#### ML Training with version1 of data as standalone run
	Click +Run

	Select Code : Deltalake

	Framework : sklearn

	Framework version : 0.23.2

	Image : ocdr/d3-datascience-sklearn:v0.23.2-16

	Startup command : python training_version1.py

	Repos > Inputs > Datasets

		Click +Dataset

		Choose "deltalake"

		Version "1"

		Mountpath "/mnt/deltalake"

	Repos > Outputs > Models

		Click +Model

		Choose "deltalake"

		Mountpath "/mnt/model"

	Click submit

#### ML Training with version2 of data as standalone run

	Click +Run

	Select Code : Deltalake

	Framework : sklearn

	Framework version : 0.23.2

	Image : ocdr/d3-datascience-sklearn:v0.23.2-16

	Startup command : python training_version2.py

	Repos > Inputs > Datasets

		Click +Dataset

		Choose "deltalake"

		Version "2"

		Mountpath "/mnt/deltalake"

	Repos > Outputs > Models

		Click +Model

		Choose "deltalake"

		Mountpath "/mnt/model"

	Trigger submit


- After the runs are complete.

- Click two runs and compare.

- Choose the run with best accuracy and proceed with below steps to deploy the model.

- Click Run > Lineage > Output Models 

- Click the model version

- Click Build Image

- Defaults are auto filled

- Click Submit button

- Wait for the image build to be successful

- Click Model > Details > Images > Image Name

- Copy the value in Image field


## Serving on Cluster 2

	Create +Deployment

	Paste the Image built in above setup

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
