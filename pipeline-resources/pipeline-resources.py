import os

import kfp
from dkube.sdk import *


dkube_url = os.getenv("DKUBE_URL")

def artifactmgr(user: str, token: str):
    import datetime
    import random
    import string

    from dkube.sdk.api import DkubeApi
    from dkube.sdk.rsrcs import DkubeCode, DkubeDataset, DkubeModel

    def generate(name):
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        return "{}-{}{}".format(
            name, timestamp, "".join([random.choice(string.digits) for n in range(4)])
        )

    api = DkubeApi(token=token)

    # Block to create the code resources here
    # Copy/Paste below lines to create N num of code resources from here
    name = "mnist-1"
    name = generate(name)
    code = DkubeCode(user, name=name)
    code.update_git_details(
        "https://github.com/oneconvergence/dkube-examples-internal/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program"
    )
    api.create_code(code)

    # Create the input dataset resources here
    name = "mnist-ds"
    name = generate(name)
    dataset = DkubeDataset(user, name=name)
    dataset.update_dataset_source(source="git")
    dataset.update_git_details(
        "https://github.com/oneconvergence/dkube-examples-internal/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/data"
    )
    api.create_dataset(dataset)

    # Create the output dataset resources here.
    output_datasets = ["output-ds-1", "output-ds-2"]
    for name in output_datasets:
        name = generate(name)
        dataset = DkubeDataset(user, name=name)
        dataset.update_dataset_source(source="dvs")
        api.create_dataset(dataset)

    # Create the output model resources here
    output_models = ["output-model-1", "output-model-2"]
    for name in output_models:
        name = generate(name)
        model = DkubeModel(user, name=name)
        model.update_model_source(source="dvs")
        api.create_model(model)

annotations = dict()
annotations['platform'] = 'Dkube'
annotations['logger'] = 'dkubepl'
annotations['dkube.garbagecollect'] = 'false'
annotations['dkube.garbagecollect.policy'] = 'all'
dkube_artifact_op = kfp.components.create_component_from_func(func=artifactmgr, base_image="ocdr/dkube_launcher:viz",annotations=annotations, output_component_file='artifactmgr.yaml')

@kfp.dsl.pipeline(name="pl-resources", description="create resources")
def resources_pipeline(username, token):
    create_datums = dkube_artifact_op(str(username), str(token))
