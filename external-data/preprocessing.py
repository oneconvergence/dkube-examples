mport json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_preprocessing_op = component_store.load_component("preprocessing")
dkube_storage_op = component_store.load_component("storage")
dkube_training_op = component_store.load_component("training")


@kfp.dsl.pipeline(
    name='external_data',
    description='utilise data from external and train'
)
def externaldata_pipeline(image,
                          code,
                          preprocessing_script,
                          ptrain_dataset,
                          train_fs_name, 
                          dataset_mount_points,
                          featureset_mount_points,
                          model_name,
                          training_script,
                          train_out_mount_points):
                          
     with kfp.dsl.ExitHandler(exit_op=storage_op("reclaim",namespace="kubeflow", uid="{{workflow.uid}}")):
            
            preprocessing = dkube_preprocessing_op(json.dumps({"image": image}),
                                            program = code,run_script=preprocessing_script,
                                            datasets=json.dumps([ptrain_dataset]), 
                                            output_featuresets=json.dumps([train_fs_name]),
                                            input_dataset_mounts=json.dumps(dataset_mount_points), 
                                            output_featureset_mounts=json.dumps(featureset_mount_points))
            
            input_volumes = json.dumps(["{{workflow.uid}}-featureset@featureset://" + train_fs_name])
            storage = dkube_storage_op("export",token, namespace="kubeflow", input_volumes=input_volumes,
                                 output_volumes=json.dumps(["{{workflow.uid}}-featureset@featureset://"+train_fs_name])).after(preprocessing)
            
       
            list_featureset = kfp.dsl.ContainerOp(
                name="list-storage",
                image="docker.io/ocdr/dkube-datascience-tf-cpu:v2.0.0-3",
                command="bash", 
                arguments=["-c", "ls /featureset"],
                pvolumes={
                         "/featureset": kfp.dsl.PipelineVolume(pvc="{{workflow.uid}}-featureset")
                         }).after(storage)
        
        
            train = dkube_training_op(token, json.dumps({"image": image}),
                                    framework="sklearn", version="0.23.2",
                                    program=code, run_script=training_script,
                                    featuresets= json.dumps([train_fs_name]), outputs=json.dumps([model_name]),
                                    input_featureset_mounts=json.dumps(featureset_mount_points),
                                    output_mounts=json.dumps(train_out_mount_points)).after(preprocessing)
            
        
        
            
        
