import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_training_op = component_store.load_component("training")



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
        version="dummy",
        run_script=run_script,
        datasets=json.dumps([str(dataset)]),
        outputs=json.dumps([str(model)]),
        input_dataset_mounts=json.dumps([str(dataset_mount_path)]),
        output_mounts=json.dumps([str(model_mount_path)]),
        envs='[{"EPOCHS": "1"}]',
    )
