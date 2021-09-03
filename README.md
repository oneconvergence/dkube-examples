This repository contains examples for various functions for DKube. Dkube supports Tensorflow, Pytorch, Sklearn frameworks for end to end development and deployments. To see examples for a particular framework/Language, choose the appropriate git branch.


### Branches

- tensorflow - contains examples using tensorflow + python
- pytorch - contains examples using pytorch + python
- sklearn - contains examples using sklearn + python
- R - contains examples using tensorflow + R
- pipelines - contains examples of kubeflow pipelines. 


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
### Examples
- [conditional-stages](conditional-stages) - this example demonstrates conditional execution of stages based on input. 
- [create-dkube-resources](create-dkube-resources) - this example demonstrates creation of dkube resources inside pipeline stages.
- [limits-requests](limits-requests) - this example demonstrates setting up limit on resources and request for these resources.
- [multiple-parallel](multiple-parallel) -  this example demonstrates how we can have multiple stages running in parallel.
- [storageop-artifacts](storageop-artifacts)  - this example demonstrates example of Dkube storage op for creating volumes.
- [training-serving](training-serving) - this example demonstrate a simple training and serving of the model using kubeflow pipelines.
- [preprocessing-pipeline](preprocessing-pipeline) - this example demonstrate a simple download of external data using kubeflow pipelines.
- [volumes-and-secret](volumes-and-secret) - this example demonstrate a sample pipeline with volume and secret
