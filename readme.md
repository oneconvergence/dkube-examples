# Training Example Repo

## Examples

 The following examples are available in this repo.

 - Chest X-Ray
 - Insurance Prediction
 - CI/CD

## 1. Insurance Prediction

 This example provides the full workflow for an example that predicts insurance costs based on individual input characteristics.  The workflow details are available in the `insurance` folder.

## 2. CI/CD

 This repo includes the details on using the DKube CI/CD capability, using the insurance example for a Training Run.  More details are available in the repo (https://github.com/oneconvergence/dkube-cicd-example).  This includes branches for a variety of CI/CD workflows.  Follow these instructions to experiment with CI/CD.  
 
### Fork the Repo

 In order to experiment with the example, you must fork this repo so that you can change the files and add a Webhook.  The remaining steps are completed in your forked repo.

### Create Resources within DKube

 The CI/CD example uses resources within your forked repo.  This section assumes that you have enough familiarity with DKube to create repos.  Use the same names for your Code, Dataset, & Model repos.

 - Create Code repo with the following fields:
   - **Name:** `<your-repo-name>`
   - **Code Source:** `Git`
   - **URL:** `<your-forked-repo>` <br><br>
   > **Note** You can get the name of the repo by selecting the green `Code` button on the right of your GitHub repo screen, and copying the HTTPS url to your copy buffer
   - **Branch:** `training`
- `Add Code` <br><br>
- Create Dataset repo with the following fields:
  - **Name:** `<your-repo-name>`
  - **Dataset Source:** `Other`
  - **URL:** `https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv`
- `Add Dataset` <br> <br>
- Create Model repo with the following fields:
  - **Name:** <your-repo-name>`
- `Add Model`

### Set up CI/CD file for Training

 The CI/CD is triggered by a GitHub commit to the repo with a Webhook.  The commit will look for a file called `.dkube-ci.yml` at the top leve of the folder within the branch.  That file will provide the details of what actions are required.

  - In this example, the `.dkube-ci.yml` file is set up to build and run a Training Run for the insurance example.  The resources for this Run were created in the previous section.
  - The YML file references a file in the `Jobs` folder called `train.yaml`
  - Navigate to the `/jobs/train.yaml` file and edit the following fields:
    - **user:** `<your-DKube-login-name>`  (2nd line)
    - **datums:** > **workspace:** > **data:** > **name:** `<your-DKube-login-name>:<your-repo-name>`  (Line 18)
      - ...**datasets:** > **name:** `<your-DKube-login-name>:<your-repo-name>`
      - ...**output:** > **name:** `<your-DKube-login-name>:<your-repo-name>`
  - `Commit Changes`

### Create GitHub Webhook

 The CI/CD actions are triggered from a GitHub Webhook.  This section explains how to set up your Webhook.

 - Start at the top repo level of your forked repo
 - Select `Settings` tab on the top & `Webhooks` from the left menu
 - Select `Add webhook` from top right of the screen
 - Fill in the following fields:
   - **Payload URL:** The url will be provided based on your system
   - **Content Type:** `application/json`
   - Select `Just the push event`
   - **Uncheck** the `Active` button for now
- `Add Webhook`

