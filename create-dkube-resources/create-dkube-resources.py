import os

import kfp
from dkube.sdk import *


dkube_url = os.getenv("DKUBE_URL")

def create_resources(user: str, token: str):
    import datetime
    import random
    import string
    from dkube.sdk import generate
    from dkube.sdk.api import DkubeApi
    from dkube.sdk.rsrcs import DkubeCode, DkubeDataset, DkubeModel

    api = DkubeApi(token=token)

    # Block to create the code resources here
    # Copy/Paste below lines to create N num of code resources from here
    name = "mnist-1"
    name = generate(name)
    code = DkubeCode(user, name=name)
    code.update_git_details(
        "https://github.com/oneconvergence/dkube-examples.git"
    )
    api.create_code(code)

    # Create the input dataset resources here
    name = "mnist-ds"
    name = generate(name)
    dataset = DkubeDataset(user, name=name)
    dataset.update_dataset_source(source="pub_url")
    dataset.update_git_details("https://s3.amazonaws.com/img-datasets/mnist.pkl.gz")
    api.create_dataset(dataset)

    # Create the output model resources here
    name = "output-model"
    name = generate(name)
    model = DkubeModel(user, name=name)
    model.update_model_source(source="dvs")
    api.create_model(model)

dkube_resources_op = kfp.components.create_component_from_func(func=create_resources, base_image="ocdr/dkube-datascience-tf-cpu:v2.0.0-6", output_component_file='create_resources.yaml')

@kfp.dsl.pipeline(name="pl-resources", description="create resources")
def resources_pipeline(username, token):
    create_datums = dkube_resources_op(str(username), str(token))
