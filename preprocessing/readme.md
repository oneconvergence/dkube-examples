# Insurance Cost Prediction Example (with Preprocessing)
 
This example trains a model to predict the cost of insurance based on a set of input characteristics for an individual.  This description provides a step-by-step recipe for using the example.  More details for the platform are available at [DKube User Guide](https://www.dkube.io/guide/guide3_x/Getting_Started.html).

This example includes a preprocessing step that creates a new version of the Dataset before training.  This is executed from a Kubeflow Pipeline.  A more complete example that does not use proprocessing is available at [Insurance Example](../insurance/readme.md).

> **Note** In the example, use only lower-case characters in the names that you create. Hyphens are acceptable in any position **other than** the first and last characters, but no other special characters should be used.

> **Note** You can choose the names for your resources in most cases.  It is recommended that you choose names that are unique to your workflow even if you are organizing them by Project.  This will ensure that there is a system-wide organization for the names, and that you can easily filter based on your own work.  A sensible approach might be to have it be something like **\<example-name\>-\<your-initials\>-\<resource-type\>**.  But this is simply a recommendation.  The specific names will be up to you.

## 1. Create Code Repo

A Model is created by running the Training Code on a Dataset.  This section explains how to create a Code repo.

- Navigate to the `Code` menu on the left
- If an optional Project is being used, choose the Project that you created in the previous step at the top of the screen
  - You only need to do this once.  It will remain the default until changed. <br><br>
- Select `+ Code`
- Fill in the required fields as follows:
  - **Name:** *`<your-code-repo>`* **(your choice of name)**
  - **Code Source:** `Git`
  - **URL:** `https://github.com/oneconvergence/dkube-examples.git`
  - **Branch:** `training`
  - Leave the other fields at their current selection 
- Submit your Code repo with the `Add Code` button at the bottom of the screen

## 2. Create JupyterLab IDE

The setup and execution are done from a JupyterLab script.  This section explains how to create the JupyterLab IDE.
 
- Navigate to the `IDEs` menu on the left
- Select `+ JupyterLab`
- Fill in the required fields in the "Basic" tab as follows:
  - **Name:** *`<your-IDE-name>`* **(your choice of name)**
  - **Code:** *`<your-code-repo>`* **(chosen during Code Repo creation)**
  - **Framework:** `tensorflow`
  - **Version:** `2.0.0`
  - Leave the other fields at their current selection 
- Submit your IDE with the `Submit` button at the bottom of the screen

## 3. Set up Resources

This section explains how to use the JupyterLab IDE to create your resources.  The variable created in this script will be used for the other scripts.
 
- Once the IDE is in the `Running` state, select the JupyterLab icon on the far right of the IDE line
  - This will open a JupyterLab tab
- Navigate to folder <code>/workspace/**\<your-code-repo\>**/preprocessing</code>
- Open `insurance-setup.ipynb`
- Change the cells in 3rd cell called `User-Defined Variables` to match your repo names
  - `CODE_REPO_NAME` = `<your-code-repo>`  **(This is the name that you used to create the Code repo)**
  - `DATASET_REPO_NAME` = `<choose a name>`  **(The setup script will create your Dataset repo with this name)**
  - `MODEL_REPO_NAME` = `<choose a name>`   **(The setup script will create your Model repo with this name)**
- Select `Run All Cells` from the top JupyterLab menu

## 4. Create and Launch Kubeflow Pipeline to Preprocess & Train Model

A Kubeflow Pipeline is used to preprocess the dataset and train the model.  The variable names for the pipeline are automatically retrieved from the setup script.

- Open the file `insurance-pipeline.ipynb`
- Select `Run All Cells` from the top JupyterLab menu
- This will create and run a Kubeflow Pipeline for the example <br> <br>
- Navigate to the `Pipelines` menu on the left, and the `Runs` tab on top
- Select the pipeline name that is running
  - It will be of the form `<your-user-name>:<your-code-repo> xxxx`
- Select the `dkube-preprocess` graph box to see the Proprocessing details
- Select the `dkube-training` graph box to see the Training Run details <br><br>
- Navigate to the `Runs` menu on the left
- You will see your Preprocessing and Training runs
  - They will be of the form `<your-user-name>-ins-pre-pl-xxxx` <br><br>
- Navigate to the `Models` menu on the left
  - Select the `Model` name `<your-model-repo\>`
- You will see that a new version of your model


