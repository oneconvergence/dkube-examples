# dkubeio-examples
This example is a modified version of https://github.com/saurabh2mishra/mlflow-demo/tree/master/sklearn-demo
- Modify conda.yaml to have correct version of protobuf

## Training
1. Install Conda v4.9 or latest
2. Clone this repo and update the conda.yaml file
3. conda env create -f conda.yaml
4. conda activate multiplan-sklearn-demo
5. python model_run.py

## Download model
1. Download the model to local directory
```
mlflow artifacts  download -r <run-id> -d <local-path>
eg: mlflow artifacts  download -r c263bdaa-9505-4dd5-81fa-f9dbf40190fc -d ./output
```

## Build image
1. Update the conda.yaml file in the downloaded path and add protobuf==3.19.4 in pip dependenicies
2. Run the below command to build the image
```
mlflow models build-docker -n <image-name> -m <local-path>/decision-tree-classifier
eg: mlflow models build-docker -n lucifer001/mlflow-sklearn-demo:demo1 -m output/decision-tree-classifier
```
3.Push the image

### Deployment
1. Select serving image which was build in the previous step.
2. Serving Port: 8000
3. Serving Url Prefix: /invocations
4. Min CPU/Max CPU: 1
5. Min Memory/Max Memory: 5G

## Prediction
1. Copy the curl command from the deployment page
2. Change the data section to
```
-d '{"data": [[17.42, 25.56, 114.5, 948.0, 0.1006, 0.1146, 0.1682, 0.06597, 0.1308, 0.05866, 0.5296, 1.667, 3.767, 58.53, 0.03113, 0.08555, 0.1438, 0.03927, 0.02175, 0.01256, 18.07, 28.07, 120.4, 1021.0, 0.1243, 0.1793, 0.2803, 0.1099, 0.1603, 0.06818]]}'
```
