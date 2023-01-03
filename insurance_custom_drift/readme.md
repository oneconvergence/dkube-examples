# Insurance example for custom data drift.

## Build Custom image
1. Clone the repo:
    - URL: https://github.com/oneconvergence/dkube-examples.git
2. Checkout `monitoring-v3` branch and change directory to `insurance_custom_drift`
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
