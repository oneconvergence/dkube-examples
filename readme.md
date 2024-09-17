# Simple Training Module

The following examples are available in this repo:

The **Insurance** example provides the full workflow for an example that predicts insurance costs based on individual input characteristics.  The example and workflow details are available in the folder [Insurance](./insurance).

## 1. Integrating MLflow with DKube for Seamless ML Training

[training_mlflow.ipynb](./insurance/training_mlflow.ipynb)

This notebook demonstrates how to leverage an ML training program developed with MLflow within the DKube environment. 

When executed inside the DKube IDE, all MLflow calls are automatically routed to DKube's enterprise-grade MLflow tracking server. This server stores the MLflow records in a database, while the DKube UI offers a multi-user interface for viewing and managing these records.

All MLflow tracking APIs can be used transparently without the need for any DKube-specific code modifications.


## 2. Running ML Training and Serving Models on DKube

[dkube_resources.ipynb](./insurance/dkube_resources.ipynb)

This notebook demonstrates how to submit an ML training program to the DKube platform and execute it. While this example covers basic usage, DKube’s API supports advanced configurations including resource specifications (GPUs, CPUs, memory) and node pinning.

Upon completion of the training, DKube automatically records all lineage information and versions the trained model. The trained model is then made available for serving.

Additionally, the notebook includes code for deploying the latest version of the trained model and testing it with sample data for inference.

## 3. Automating DKube Training and Serving with Kubeflow Pipelines

[pipeline.ipynb](./insurance/pipeline.ipynb)

This notebook demonstrates how to automate DKube training and serving workflows using Kubeflow Pipelines.

DKube extends Kubeflow components by implementing specialized operators that integrate with the KFP SDK, providing a seamless interface for submitting components to the DKube platform.

DKube supports KFP components for various tasks, including training, serving, and preprocessing.
