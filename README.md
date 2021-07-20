This repository contains examples for various functions for DKube. Dkube supports Tensorflow, Pytorch, Sklearn frameworks for end to end development and deployments. To see examples for a particular framework/Language, choose the appropriate git branch.


### Branches

- tensorflow - contains examples using tensorflow + python
- pytorch - contains examples using pytorch + python
- sklearn - contains examples using sklearn + python
- R - contains examples using tensorflow + R
- pipelines - contains examples of kubeflow pipelines. 

### Examples

Each pipeline example contains a pipline definition (.py file) and a config.yaml file. config.yaml shows referance values to run the pipeline. In case DKube resources needs to be created, they are specified under code, datasets and models. Pipeline arguments are specified under arguments.

Some values of `__xxx__` form needs to be provided by the user.