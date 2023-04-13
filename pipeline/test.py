import sys,json, os
import kfp
import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler
import kfp.dsl as dsl

import string

dkube_training_op = components.load_component_from_url('https://raw.githubusercontent.com/oneconvergence/dkube/main/components/training/component.yaml')
dkube_serving_op = components.load_component_from_url('https://raw.githubusercontent.com/oneconvergence/dkube/main/components/serving/component.yaml')

training_program = "xray-larryc"
training_script = "python chest-xray/training.py"
input_training_dataset = "xray-lc"
model_name = "xray-lc"
input_dataset_mount = ['/data']
output_model_mount = "/model"
serving_job_name = "ray-lc"

@kfp.dsl.pipeline(
    name="xray-pl",
    description='Chest XRay Pipeline'
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
    
    serving     = dkube_serving_op(model=train.outputs['artifact'], device='cpu',
                                    name=serving_job_name,
                                    serving_image=json.dumps({"image": "ocdr/tensorflowserver:2.0.0"}),
                                    auth_token=token, min_replicas = '1',
                                    production="true").after(train)
