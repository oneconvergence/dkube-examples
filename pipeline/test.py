@kfp.dsl.pipeline(
    name=f"{DKUBE_TRAINING_CODE_NAME}-pl",
    description='xray-training-pl'
)
def xray_pipeline(token):    
    train       = dkube_training_op(container=json.dumps({"image": "ocdr/dkube-datascience-tf-cpu:v2.0.0-17"}),
                                    framework="tensorflow", version="2.0.0",
                                    program=str(training_program), 
                                    run_script=str(training_script),
                                    datasets=json.dumps([str(input_training_dataset)]), 
                                    outputs=json.dumps([str(model_name)]),
                                    input_dataset_mounts=json.dumps(input_dataset_mount),
                                    output_mounts=json.dumps([str(output_model_mount)]),
                                    auth_token=token)
