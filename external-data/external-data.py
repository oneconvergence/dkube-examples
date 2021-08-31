import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_preprocessing_op = component_store.load_component("preprocess")
dkube_storage_op = component_store.load_component("storage")
dkube_training_op = component_store.load_component("training")


@kfp.dsl.pipeline(
    name="external_data", description="utilise data from external and train"
)
def externaldata_pipeline(
    code,
    preprocessing_script,
    dataset,
    dataset_mount_points,
    token,
):

    preprocessing = dkube_preprocessing_op(
        auth_token=str(token),
        container=json.dumps({"image": "ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-5"}),
        program=str(code),
        run_script=str(preprocessing_script),
        outputs = [str(dataset)],
        output_mounts = [str(dataset_mount_points)],
    )

