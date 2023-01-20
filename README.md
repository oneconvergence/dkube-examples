## Loan Data Accuracy Example

 This example uses Delta Lake to source 2 versions of data that is then used to determine which version is more accurate at determining whether a loan should be provided.  	A WebApp has been created that uses Kafka to provide input to the deployed model.

 This example uses one cluster (**Cluster 1**) to train the models, and a different cluster (**Cluster 2**) to serve the model that does the best job.

## Training on Cluster 1

 Cluster 1 is used to train the models and compare their accuracy.

### Create Code Resource

 - Select `Code` repo from left menu, then select `+ Code` button

   - **Name:** `deltalake` (**You can choose a different name for this and other resources**)
 
   - **Code Source:** `Git`

   - **URL:** `https://github.com/oneconvergence/dkube-examples/tree/deltalake`

 - Leave the other fields at their current value and `Submit`

### Create Dataset Resource

 - Select `Datasets` from the left menu, then select `+ Dataset` button

   - **Name:** `deltalake`

   - **Versioning:** `None`  (**Note: This is not the default**)
 
   - **Dataset Source:** `Deltalake`

   - **Table Source:** `S3`

   - **Table Path:** `dkube-deltalake/loans.delta`

 - Leave the other fields at their current value and `Submit`

### Create Model Resource

 - Select `Models` from the left menu, then select `+ Model` button

   - **Name:** `deltalake`

 - Leave the other fields at their current value and `Submit`	

### Create a Jupyterlab IDE

 - Select `IDEs` from the left menu, then select `+ JupyterLab` button

   - **Name:**` deltalake`

   - **Framework:** `sklearn`  (**The Version & Image will fill in automatically with the Framework**)

 - Leave the other fields at their current value and `Submit`

### ML Training inside notebook

 - Launch JupyterLab from the icon at the far right after the IDE is running (this may take several minutes)

 - Navigate to `workspace/deltalake`  (**If you chose a different name than "deltalake" for your code use that name instead**)

#### Train with Version 1 of Data

 - Open `training_version1.ipynb`

 - Select `Run` -> `Run All Cells`

#### Train with Version 2 of Data

 - Open `training_version2.ipynb`

 - Select `Run` > `Run All Cells`

### ML Training with Version 1 of Data as Standalone Run

 - Select `Runs` from left menu, then select `+ Run` > `Training Run`

 - `Basic` Tab
 
   - **Name:** `deltalake-run1`

   - **Code:** `deltalake`  (**If you chose a different name for your code, use it here instead**)

   - **Framework:** `sklearn`  (**The correct version and image will be filled in**)

   - **Startup Command:** `python training_version1.py`

 - `Repos` Tab

   - **Inputs:** Choose `+ Dataset`

     - Choose `deltalake`  (**Or the name that you chose for your Dataset**)

     - **Version:** `1`

     > **Note** It will default to Version 2, so you must change it

     - **Mountpath:** `/mnt/deltalake`

   - **Outputs:** Choose `+ Model`

     - Choose `deltalake`  (**Or the name that you chose for your Model**)

     - **Mountpath:** `/mnt/model`

 > **Note** There is a `Model` section in the Inputs.  Make sure that you enter the Model in the **Output** section only
 
 - Leave the other fields at their current value and `Submit`

### ML Training with Version 2 of Data as Standalone Run

 - Select `Runs` from left menu, then select `+ Run` > `Training Run`

 - `Basic` Tab
 
   - **Name:** `deltalake-run2`

   - **Code:** `deltalake`  (**If you chose a different name for your code, use it here instead**)

   - **Framework:** `sklearn`  (**The correct version and image will be filled in**)

   - **Startup Command:** `python training_version2.py`

   > **Note** If you use `Clone` to create the 2nd Run, make sure that you change the startup command to Version 2

 - `Repos` Tab

   - **Inputs:** Choose `+ Dataset`

     - Choose `deltalake`  (**Or the name that you chose for your Dataset**)

     - **Version:** `2`

     > **Note** If you use `Clone` to create the 2nd Run, make sure that you change the version to Version 2

     - **Mountpath:** `/mnt/deltalake`

   - **Outputs:** Choose `+ Model`

     - Choose `deltalake`  (**Or the name that you chose for your Model**)

     - **Mountpath:** `/mnt/model`

    > **Note** There is a `Model` section in the Inputs.  Make sure that you enter the Model in the **Output** section only
 
 - Leave the other fields at their current value and `Submit`

## Compare the Runs for Accuracy

- Wait for Runs to `complete`

- Select the 2 runs and `Compare`

- Choose the run with best accuracy and proceed to deploy the model as explained in the next section

## Build the Model Image & Save in External Repository

- Select `Run` that had the best accuracy

- Select `Lineage` tab, then select `Outputs` >  `Models` 

  - Select the Model link

- Select `Images` tab, then `Build Image` button

  - Defaults are auto filled

- Select `Submit` button

- Wait for the `Image Name` to show up on the screen

- Select `Image Name`

- Copy the value in `Image` field to your copy buffer (**There is an icon to do that**)

## Serving on Cluster 2

 Move from **Cluster 1** to **Cluster 2** in order to complete the deployment.
 
 - Select `Deployments` from left menu, then select `+ Deployment` button

   - **Name:** deltalake
   
   - **Serving Image:** Paste the Image built in the previous step

   > **Note** After you paste in the image name, click anywhere else on the screen rather than using the "Enter" key.  If you use the "Enter" key it will pick up the wrong image.

   - **Deployment:** `Production`

   - **Deploy Using:** `CPU`

   - **Event Source:** `Kafka`

   - **Brokers:** `dkube-kafka-cp-kafka.dkube-kafka:9092`

   - **Topics:** `<your login username>`

   - **Consumer Group:** `training`

 - Leave the other fields at their current value and `Submit`

 - Wait for "Deployment" to get to `Running` state

## Test Inference

 - WebApp will be available @ dkubeserving-clusterip:31333
	
 - Input the following values
	
   - **Kafka broker endpoint:** `dkube-kafka-cp-kafka-headless.dkube-kafka:9092`
	
   - **Kafka topic:** `<username>`
	
   - **Select Version:** `version2`
	
   - **Number of times to send:** `1`
	
 - Select `Predict` button
