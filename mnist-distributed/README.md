# DISTRIBUTED TRAINING MNIST EXAMPLE 

## Directory Structure
   1. Single host, multiple device synchronous training - which uses [**MirrorStrategy**](https://www.tensorflow.org/api_docs/python/tf/distribute/MirroredStrategy). **Code is in mnist-distributed/mirrored_mnist.py.**
   2. On a cluster of many machines, each hosting one or multiple GPUs (multi-worker distributed training) - which uses [**MultiworkerMirrorStrategy**](https://www.tensorflow.org/api_docs/python/tf/distribute/MultiWorkerMirroredStrategy). **Code is in mnist-distributed/multiworker_mnist.py**
      
**Note:** The way TF distributed works is, TF operator sets the distributed cluster configuration in an env named TF_CONFIG, It automatically inserts the ENV in each worker, chief and parameter server.It is handled between DKube and TFJob operators.


## Create code repo
- Name: dkube-examples
- Project source: Git
- Git URL: https://github.com/oneconvergence/dkube-examples.git
- Branch: tensorflow

## Create dataset repo
- Name: mnist
- Dataset source: Other
- URL: https://s3.amazonaws.com/img-datasets/mnist.pkl.gz

## Create a model
- Name: mnist
- Keep default for others

## Run training job
 - Runs->+Training Run.
 - Code: dkube-examples
 - Framework: Tensorflow
 - Version: 
   - For mirrored :  2.0.0 or 2.0.0-gpu
   - For multiworker : 2.3.0-gpu 
 - Start-up script: 
   - For training using **mirrored strategy**: `python mnist-distributed/mirrored_mnist.py` 
   - For training using **multi worker strategy**: `python mnist-distributed/multiworker_mnist.py`
 - Repos->Inputs->Datasets: select mnist dataset enter mountpath as /mnist
 - Repos->Outputs->Model: select mnist model and enter mountpath as /model
 - **Allocate GPUS**
 - **Select Distributed workloads : Automatic Distribution**
 - Submit
