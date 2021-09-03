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
    dataset,
    dataset_mount_points,
    token,
):
    command ="wget https://dkube.s3.amazonaws.com/datasets/titanic.zip ; unzip titanic.zip -d " + str(dataset_mount_points)
    preprocessing = dkube_preprocessing_op(
            container=json.dumps({"image": "bash:latest"}),
        run_script=command,
        outputs = [str(dataset)],
        output_mounts = [str(dataset_mount_points)],
    )

