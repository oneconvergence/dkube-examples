import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_training_op = component_store.load_component("training")
dkube_serving_op = component_store.load_component("serving")


@kfp.dsl.pipeline(
    name="train-serve",
    description="pipeline with dkube training and serving components",
)
def training_serving(
    code,
    run_script,
    transformer_script,
    dataset,
    dataset_mount_path,
    model,
    model_mount_path,
    token,
):

    train = dkube_training_op(
        auth_token=str(token),
        container='{"image":"ocdr/dkube-datascience-tf-cpu:v2.0.0"}',
        framework="tensorflow",
        version="2.0.0",
        program=str(code),
        run_script=str(run_script),
        datasets=json.dumps([str(dataset)]),
        outputs=json.dumps([str(model)]),
        input_dataset_mounts=json.dumps([str(dataset_mount_path)]),
        output_mounts=json.dumps([str(model_mount_path)]),
        envs='[{"EPOCHS": "1"}]',
    )

    _ = dkube_serving_op(
        str(token),
        train.outputs["artifact"],
        device="cpu",
        serving_image='{"image":"ocdr/tensorflowserver:2.0.0"}',
        transformer_image='{"image":"ocdr/dkube-datascience-tf-cpu:v2.0.0"}',
        transformer_project=str(code),
        transformer_code=str(transformer_script),
    ).after(train)
