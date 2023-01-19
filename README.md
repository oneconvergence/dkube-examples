## Training on Cluster 1
#### Create code resource
name : deltalake

github url - https://github.com/oneconvergence/dkube-examples/tree/deltalake

#### Create Dataset resource
	name : deltalake

	Versioning : None

	Dataset Source : Deltalake

	Table Source : s3

	Table Path : dkube-deltalake/loans.delta

#### Create Model resource
	name : deltalake

#### Create a Jupyterlab IDE
	Framework : sklearn

	Framework version : 0.23.2

	Image : ocdr/d3-datascience-sklearn-multiuser:v0.23.2-16

#### ML Training inside notebook
	Goto workspace/deltalake

###### Train with version 1 of data
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
