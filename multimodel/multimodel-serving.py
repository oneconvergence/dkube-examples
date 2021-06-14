import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_serving_op = component_store.load_component("serving")
storage_op = component_store.load_component("storage")


@kfp.dsl.pipeline(
    name="multimodel-pl", description="sample multimodel pipeline with dkube components"
)
def multimodel_pipeline(model):

    with kfp.dsl.ExitHandler(
        exit_op=storage_op("reclaim", namespace="kubeflow", uid="{{workflow.uid}}")
    ):

        model_volume = json.dumps(["{{workflow.uid}}-model@model://" + str(model)])

        storage = storage_op("export", namespace="kubeflow", input_volumes=model_volume)

        list_models = kfp.dsl.ContainerOp(
            name="container-op",
            image="docker.io/ocdr/dkube-datascience-tf-cpu:v2.0.0-3",
            command="bash",
            arguments=["-c", "ls /model"],
            pvolumes={"/model": kfp.dsl.PipelineVolume(pvc="{{workflow.uid}}-model")},
        ).after(storage)

        serving = dkube_serving_op(
            model=str(model),
            device="cpu",
            serving_image='{"image":"ocdr/inf-multimodel:latest"}',
        ).after(storage)
