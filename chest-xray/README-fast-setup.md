# Chest X-Ray Example Fast Setup

This file explains how to get your file set up with scripts.  It minimizes your setup effort.

## 1. Create the Code Repo

- Select `Code` menu on the left, then `+ Code`, and fill in the following fields:
  - **Name:** `chest-xray`  **(Or choose your own name as `<your-code-repo>`)**
  - **Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples.git`
  - **Branch:** `training`
- Leave the rest of the fields at their current value
- `Add Code`

## 2. Create and Launch JupyterLab

- Select `IDEs` menu on the left, then `+ JupyterLab`, and fill in the following fields:
  - **Basic Tab**
    - **Name:** `Choose an IDE name`
    - **Code:** *`<your-code-repo>`*  **(Chosen during Code repo creation)**
    - **Framework:** `tensorflow`
    - **Framework Version:** `2.0.0`
    - **Image:** `ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-xx`   **(This should be the default, 'xx' may differ)**
    - Leave the rest of the Basic fields at their current value<br><br>
  - **Repos Tab**
    - **Inputs / Datasets:** *`<your-dataset-repo>`*   **(Chosen during Dataset repo creation)**
      - **Mount Path:** `/data`
- Leave the rest of the fields at their current value
- `Submit`

## 3. Create Resources for Pipeline and Monitor

- Within the `JupyterLab` tab, open `resources.ipynb`
- Change the following variables in the 3rd cell `User-Defined Variables`
  - DKUBE_TRAINING_CODE_NAME = `<your-code-repo>`
  - TRAINING_DATASET = `<your-dataset-repo>`
  - DKUBE_MODEL_NAME = `<your-model-name>`
  - Leave the other variables at their current value
- `Run All Cells`

> **Note** Your repos are set up, and you can then experiment with JupyterLab, create Training runs, deploy models, or create model monitors

