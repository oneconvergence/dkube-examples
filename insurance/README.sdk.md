## MODEL MONITOR (SDK)

### Create Model Monitor

1. From **workspace/insurance/insurance** open [modelmonitor.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/modelmonitor.ipynb) and run all the cells. New model monitor will be created.

### Data Generation
1. Open [data_generation.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/data_generation.ipynb) notebook for generating predict and groundtruth datasets.
2. In 1st cell, Update Frequency according to what you set in Modelmonitor. If the d3qatest tag was provided replace it with to use frequency in minutes. For eg: for 5 minutes replace it with `5m` else use `5h` for hours assuming Frequency specified in monitor was 5.
3. Then Run All Cells. It will start Pushing the data, by default it will push the data to local.

### Retraining
1. Open [resources.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/resources.ipynb) and set INPUT_TRAIN_TYPE = 'retraining' in the 1st cell and run all the cells.
2. Open train.ipynb and run all the cells.
3. This creates a new version of dataset and a new version of model
   - New dataset version will be created for 'insurance-training-data' dataset
   - New model version will be created for 'insurance-model' model
4. From **workspace/insurance/insurance** open modelmonitor.ipynb and run the Retraining cell. It will update the dataset and model version in the existing model monitor.

### Cleanup
1. After your expirement is complete, 
   - Open [resources.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insuranceresources.ipynb) and set CLEANUP=True in last Cleanup cell and run.
   - Open [modelmonitor.ipynb](https://github.com/oneconvergence/dkube-examples/tree/monitoring/insurance/modelmonitor.ipynb) and set CLEANUP=True in last Cleanup cell and run.
