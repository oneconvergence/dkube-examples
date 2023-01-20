# Insurance example for custom data drift.

## Build Custom image
1. Clone the repo:
    - URL: https://github.com/oneconvergence/dkube-examples.git
2. Checkout `monitoring` branch and change directory to `insurance_custom_drift`
3. Build the image using the following command:
    > docker build . -t {image-name:tag} -f Dockerfile
    - use image name and tag of you choice. 
      - eg: `ocdr/insurance_custom:v1`
    - Push it to dockerhub(optional).
    - > **Note:** The image must be pullable from docker hub or locally present in the monitoring setup. 

## Import Deployment:
1. In DKube go to Deployments.
2. Click on `+Import`
3. **Name:** *`<your-deployment-name>`* **(your choice of deployment-name)**
4. Leave the other fields at their current selection
5. Click on import. 


## Create Model Monitor:
1. From Deployment actions use the last action i.e add model monitor action.
2. Select **Model Type** as **Regression**
3. Select **Data type** as **Tabular**
4. Go to **Drift** and enable drift
5. Select the algorithm **Custom**.
6. Provide the previous build image name in **Docker Image** field,
   - eg: `ocdr/insurance_custom:v1`
7. Fill start-up command `bash custom.sh`
8. Submit.
9.  Go to Schema page and verify schema. 
10. Close the Schema page, select the model monitor and start.


## Samples
Samples for schema, distributions and drift metric files can be found in samples folder. 

### 1. schema.csv
`schema.csv` requies four columns
  - class: class of the feature
    - continous or categorical
  - label: Name of the feature in train data.
  - type: type of the feature,
    - input_feature: if feature is a input feature
    - prediction_output: if feature is output feature.
    - row_id: if the feature is unique sample identifier
    - timestamp: if the feature is a timestamp column
  - selected: Whether you want feature to be monitor for drift,
    - true
    - false
In `schema.csv` each row belong to each feature, and it need to be loaded as dataframe to be used to update schema.

### 2. baseline.json
`baseline.json` shows how the train data disribution should looks like. 
Each feature is having a discribtion feild which is required to have mean, std, min, max for continous features and top, unique for categorical features.
>Tip: Use Pandas inbuild [describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html) function to calculate distributions.

### 3. features_scores.json
`features.json` file containes feature scores of input features of the model in a key, value pair arrangement. 

### 4. drift_metrics.json
`drift_metrics.json` containes the drift scores and predict data distributions. The key shoud be `scores` and `distributions` only. scores have drict scores feature wise. distribution data arrangement is similar to baseline data. 
