import sys,json, os
import kfp
import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler
import kfp.dsl as dsl
from kubernetes import client as k8s_client

dkube_training_op = components.load_component_from_url('https://raw.githubusercontent.com/oneconvergence/dkube/main/components/training/component.yaml')
dkube_serving_op = components.load_component_from_url('https://raw.githubusercontent.com/oneconvergence/dkube/main/components/serving/component.yaml')

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6ImxhcnJ5YzEyMDAiLCJyb2xlIjoiZGF0YXNjaWVudGlzdCxtbGUscGUiLCJkZXBsb3kiOmZhbHNlLCJleHAiOjQ5MjA2MjM2NTUsImlhdCI6MTY4MDYyMzY1NSwiaXNzIjoiRGt1YmUifQ.36Q6aU8q0YzN70wylWPfmOWPCooCs5pmjHj2o5HRkkd322Dn0Oq5EOLfbrNP5GFEhVGiDXK7wCVzMIFzaLW7eV1RUSsYQHAFLAsENEZvXoOuUEzpN823tg5Ovs5J8tuqNQCd_5_LGZP9jS3M2RhL8IX3jaNsv68WBhn70zXixQONR8YFse0xITyTO5AvTQbJqbqLEY7hSEM0CoczU_v-Et_J3FDR2Qus7_Eb_51K1btvnZ_EGvmYQTTufzEY-jMUunQUGz3ckDOy5mS5gK72axyVh9HRhFSKTsJwSiGL0BS_upuZQjuSVaLuQiBrCo8XtTrArKV8zJH9hDpyq5gXeA"
client = kfp.Client(
    host="http://istio-ingressgateway.istio-system/pipeline",
    existing_token=token,
    namespace="larryc1200")

pl_run_name = "xray-pl"
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
                                    serving_image=json.dumps({"image": "ocdr/tensorflowserver:2.0.0"}),
                                    auth_token=token, min_replicas = '1',
                                    production="true").after(train)

#client.create_run_from_pipeline_func(xray_pipeline, run_name=pl_run_name, arguments={'token':token})

