# Training Example Repo

## Examples

 The following examples are available in this repo.

 - Chest X-Ray
 - Insurance Prediction
 - CI/CD

## 1. Insurance Prediction

 The **Insurance** example provides the full workflow for an example that predicts insurance costs based on individual input characteristics.  The example and workflow details are available in the folder [Insurance](./insurance).

 ## 2. Chest X-Ray

 The **Chest X-Ray** example trains a model based on X-Rays that include normal and diseased images.  It predicts whether an X-Ray is healthy.  The example and workflow details are available in the folder [Chest X-Ray](./chest-xray).

## 2. CI/CD

 This repo includes the details on using the DKube CI/CD capability, using the chest X-Ray example for a Training Run.  More details are available in the repo [CI/CD Examples](https://github.com/oneconvergence/dkube-cicd-example).  This includes branches for a variety of CI/CD workflows.  Follow these instructions to experiment with CI/CD.  
 
### Fork the Repo

 In order to experiment with the example, you must fork this repo so that you can change the files and add a Webhook.  The remaining steps are completed in your forked repo.
 
> **Note** Ensure that you **uncheck** the "Copy the `tensorflow` branch only".  Otherwise, the `training` branch will not be forked.  This example uses the `Training` branch.

### Create Resources within DKube

 The CI/CD example uses resources within your forked repo.  This section assumes that you have enough familiarity with DKube to create repos.  It will makes things simpler if you use short names for your Code, Dataset, & Model repos, and make them all the same name.

 > **Note** The recommended format for the repo names is `xray-<your-initials>-cicd`.  This will allow you to find your resources among others using the same system.

 - Create Code repo with the following fields:
   - **Name:** `<your-code-repo>`
   - **Code Source:** `Git`
   - **URL:** `<your-forked-repo>.git` <br><br>
   > **Note** You can get the name of the repo by selecting the green `Code` button on the right of your GitHub repo screen, and copying the HTTPS url to your copy buffer
   - **Branch:** `training`
- `Add Code` <br><br>
- Create Dataset repo with the following fields:
  - **Name:** `<your-data-repo>`
  - **Dataset Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples/tree/training/chest-xray/data/chest-xray-mini`
  - > **Note** You will be getting your dataset from the original repo
- `Add Dataset` <br> <br>
- Create Model repo with the following fields:
  - **Name:** `<your-model-repo>`
- `Add Model`

### Set up CI/CD file for Training

 The CI/CD is triggered by a GitHub commit to the repo with a Webhook.  The commit will look for a file called `.dkube-ci.yml` at the top level of the folder within the branch.  That file will provide the details of what actions are required.
 
 > **Note** Ensure that you are in the `training` branch

  - In this example, the `.dkube-ci.yml` file is set up to build and run a Training Run for the Chest X-Ray example.  The resources for this Run were created in the previous section.
  - The YML file references a file in the `Jobs` folder called `train.yaml`
  - Navigate to the `/jobs/train.yaml` file and edit the following fields:
    - **user:** `<your-DKube-login-name>`  (2nd line)
    - **datums:** > **workspace:** > **data:** > **name:** `<your-DKube-login-name>:<your-repo-name>`  (Line 18)
      - ...**datasets:** > **name:** `<your-DKube-login-name>:<your-repo-name>`
      - ...**output:** > **name:** `<your-DKube-login-name>:<your-repo-name>`
  - `Commit Changes`

### Create GitHub Webhook

 The CI/CD actions are triggered from a GitHub Webhook.  This section explains how to set up your Webhook.
 
 > **Note** Ensure that you are in the `training` branch

 - Start at the top repo level of your forked repo
 - Select `Settings` tab on the top & `Webhooks` from the left menu
 - Select `Add webhook` from top right of the screen
 - Fill in the following fields:
   - **Payload URL:** The url will be provided based on your system
   - **Content Type:** `application/json`
   - Select `Just the push event`
   - Ensure that the `Active` checkbox is checked
 - `Add Webhook`

### Edit and Commit File in Repo

 Once the Webhook is created and active, it will trigger when a commit is made to the GitHub repo.  This section provides a simple change to initiate the trigger.

 > **Note** Ensure that you are in the `training` branch

 - Navigate to the `chest-xray` folder
 - Select the file `README.md`
 - Edit the file and add some simple change, such as a comment
 - `Commit Changes`
 
 ### View CI/CD Workflow

  The commit will trigger the CI/CD workflow.  You can follow the progress and status from the `Images` screen in Dkube, as explained here.

  - Navigate to `Images` menu on the right of the DKube screen
  - Choose the `Builds` tab on the top
  - Your build will be either in progress or complete.  It will have a `create at` time of a minute or less.
  - Select the build name to see the progress and status
  - Wait for the build to complete

### View the Run and Models Created

 After the CI/CD workflow has been completed, you can see the Training Run that was built and run, and the resulting Model.

 - Navigate to `Runs` menu on the left
 - Your Run will be near the top, and will either be in progress or complete
 - After the Run is complete, navigate to `Models` menu on the left
 - Expand the Model with `<your-model-repo>`
 - You will see a new version of the Model has been created

 > **Note** After the CI/CD has run, it it **important** that you go back and **uncheck** the `Active` checkbox in your Webhook.  Otherwise, every commit will trigger that CI/CD workflow.
