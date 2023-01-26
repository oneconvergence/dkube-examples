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
   - **URL:** `<your forked repo>` <br><br>

   > **Note** You can get the name of the repo by selecting the green `Code` button on the right of your GitHub repo screen, and copying the HTTPS url to your copy buffer

   - **Branch:** `training`
- `Add Code`

- Create Dataset repo with the following fields:
  - **Name:** `<your-repo-name>`
  - **Dataset Source:** `Other`
  - **URL:** `https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv`
- `Add Dataset`

- Create Model repo with the following fields:
  - **Name:** <your-repo-name>`
- `Add Model`


