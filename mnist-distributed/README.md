# DISTRIBUTED TRAINING MNIST EXAMPLE 

## Directory Structure
   1. Single host, multiple device synchronous training - which uses **MirrorStrategy**. **Code is in mnist-distributed/mirrored_mnist.py.**
   2. On a cluster of many machines, each hosting one or multiple GPUs (multi-worker distributed training) - which uses **MultiworkerMirrorStrategy.
      Code is in mnist-distributed/multiworker_mnist.py**
      
**Note:** The way TF distributed works is, TF operator sets the distributed cluster configuration in an env named TF_CONFIG, It automatically inserts the ENV in each worker, chief and parameter server.
It is handled between DKube and TFJob operators.


## Create code repo
- Name: distributed-training
- Project source: Git
- Git URL: https://github.com/oneconvergence/dkube-examples.git
- Branch: tensorflow

## Create dataset repo
- Name: mnist
- Dataset source: Other
- URL: https://s3.amazonaws.com/img-datasets/mnist.pkl.gz

## Create a model
- Name: distributed-model
- Keep default for others

## Run training job
 - Runs->+Training Run.
 - Code: distributed-training
 - Framework: Tensorflow
 - Version: 
   - For mirrored : 2.0.0-gpu
   - For multiworker : 2.3.0-gpu 
 - Start-up script: 
   - For mirrored : python mnist-distributed/mirrored_mnist.py 
   - For multiworker : python mnist-distributed/multiworker_mnist.py
 - Repos->Inputs->Datasets: select mnist dataset enter mountpath as /mnist
 - Repos->Outputs->Model: select distributed-model and enter mountpath as /model
 - **Allocate GPUS**
 - **Select Distributed workloads : Automatic Distribution**
 - Submit
