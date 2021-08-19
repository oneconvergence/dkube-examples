This repository contains examples for various functions for DKube. Dkube supports Tensorflow, Pytorch, Sklearn frameworks for end to end development and deployments. To see examples for a particular framework/Language, choose the appropriate git branch.


### Branches

- tensorflow - contains examples using tensorflow + python
- pytorch - contains examples using pytorch + python
- sklearn - contains examples using sklearn + python
- R - contains examples using tensorflow + R
- pipelines - contains examples of kubeflow pipelines. 

### Examples

- [mnist](mnist) - this example demonstrates end to end workflow of dkube from development to deployment. 
- [titanic](titanic) - this example demonstrates on how to use featuresets and leaderboard in DKube
- [noteboks](notebooks) - this directory contains notebooks showing DKube API/SDK, Kubeflow Pipelines and DKube storage op usage

### Accessing Code from inside container
Dkube pipeline components make all the code repos available at /mnt/dkube/home//workspace. Following example shows how to access a particular script file from your code repo in dkube component.

```python3
@kfp.dsl.pipeline(name="homedir-pl", description="code from home dir")
def homedircode_pipeline(
    code, dataset, model, dataset_mount_path, model_mount_path, token, user
):

    run_script = (
        "python /mnt/dkube/home/"
        + str(user)
        + "/workspace/"
        + str(code)
        + "/mnist/train.py"
    )

    train = dkube_training_op(
        auth_token=str(token),
        container='{"image":"ocdr/dkube-datascience-tf-cpu:v2.0.0"}',
        framework="custom",
        run_script=run_script,
        datasets=json.dumps([str(dataset)]),
        outputs=json.dumps([str(model)]),
        input_dataset_mounts=json.dumps([str(dataset_mount_path)]),
        output_mounts=json.dumps([str(model_mount_path)]),
    )
```
