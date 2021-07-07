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
    featureset,
    dataset_mount_points,
    featureset_mount_points,
    model,
    training_script,
    train_out_mount_points,
    token,
):

    with kfp.dsl.ExitHandler(
        exit_op=dkube_storage_op(
            "reclaim",
            auth_token=str(token),
            namespace="kubeflow",
            uid="{{workflow.uid}}",
        )
    ):

        # preprocessing_script = str(preprocessing_script)
        # preprocessing_script = preprocessing_script.replace("__TOKEN__", str(token))
        preprocessing = dkube_preprocessing_op(
            auth_token=str(token),
            container=json.dumps({"image": "ocdr/d3-datascience-sklearn:v0.23.2-1"}),
            program=str(code),
            run_script=str(preprocessing_script),
            datasets=json.dumps([str(dataset)]),
            output_featuresets=json.dumps([str(featureset)]),
            input_dataset_mounts=json.dumps([str(dataset_mount_points)]),
            output_featureset_mounts=json.dumps([str(featureset_mount_points)]),
        )

        input_volumes = json.dumps(
            ["{{workflow.uid}}-featureset@featureset://" + str(featureset)]
        )
        storage = dkube_storage_op(
            "export",
            auth_token=str(token),
            namespace="kubeflow",
            input_volumes=input_volumes,
            output_volumes=json.dumps(
                ["{{workflow.uid}}-featureset@featureset://" + str(featureset)]
            ),
        ).after(preprocessing)

        list_featureset = kfp.dsl.ContainerOp(
            name="list-storage",
            image="docker.io/ocdr/dkube-datascience-tf-cpu:v2.0.0-3",
            command="bash",
            arguments=["-c", "ls /featureset"],
            pvolumes={
                "/featureset": kfp.dsl.PipelineVolume(pvc="{{workflow.uid}}-featureset")
            },
        ).after(storage)

        train = dkube_training_op(
            auth_token=str(token),
            container=json.dumps({"image": "ocdr/d3-datascience-sklearn:v0.23.2-1"}),
            framework="sklearn",
            version="0.23.2",
            program=str(code),
            run_script=str(training_script),
            featuresets=json.dumps([str(featureset)]),
            outputs=json.dumps([str(model)]),
            input_featureset_mounts=json.dumps([str(featureset_mount_points)]),
            output_mounts=json.dumps([str(train_out_mount_points)]),
        ).after(preprocessing)
