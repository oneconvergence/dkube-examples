import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_preprocessing_op = component_store.load_component("preprocess")


@kfp.dsl.pipeline(
    name="preprocessing_pipeline", description="utilise data from external and copy into local dataset"
)
def preprocessing_pipeline(
    code,
    preprocessing_script,
    dataset,
    dataset_mount_points,
    token,
):

    preprocessing = dkube_preprocessing_op(
        container=json.dumps({"image": "ocdr/dkube-datascience-tf-cpu-multiuser:v2.0.0-5"}),
        program=str(code),
        run_script=str(preprocessing_script),
        outputs = [str(dataset)],
        output_mounts = [str(dataset_mount_points)],
    )

