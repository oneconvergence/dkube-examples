import sys,json, os
import kfp
import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler
import kfp.dsl as dsl
from kubernetes import client as k8s_client

# User-specific variables
core_repo_name = "xray-larryc"
data_repo_name = "xray-lc"
model_repo_name = "xray-lc"

# Fixed variables
input_dataset_mount = ['/data']
output_model_mount = "/model"
training_script = "python chest-xray/training.py"
pl_run_name = "xray-pl"

# Set up Pipeline components
dkube_training_op = components.load_component_from_url('https://raw.githubusercontent.com/oneconvergence/dkube/main/components/training/component.yaml')
dkube_serving_op = components.load_component_from_url('https://raw.githubusercontent.com/oneconvergence/dkube/main/components/serving/component.yaml')

# Get environmental variables
DKUBE_ACCESS_TOKEN = os.environ.get("DKUBE_USER_ACCESS_TOKEN") 
DKUBE_USERNAME = os.environ.get("DKUBE_USER_LOGIN_NAME")

# Set up pipeline access
host_url="http://istio-ingressgateway.istio-system/pipeline"
client = kfp.Client(
    host=host_url,
    existing_token=DKUBE_ACCESS_TOKEN,
    namespace=DKUBE_USERNAME)

@kfp.dsl.pipeline(
    name="xray-pl",
    description='Chest XRay Pipeline'
)
def xray_pipeline(token):    
    train       = dkube_training_op(container=json.dumps({"image": "ocdr/dkube-datascience-tf-cpu:v2.0.0-17"}),
                                    framework="tensorflow", version="2.0.0",
                                    program=str(code_repo_name), 
                                    run_script=str(training_script),
                                    datasets=json.dumps([str(data_repo_name)]), 
                                    outputs=json.dumps([str(model_repo_name)]),
                                    input_dataset_mounts=json.dumps(input_dataset_mount),
                                    output_mounts=json.dumps([str(output_model_mount)]),
                                    auth_token=DKUBE_ACCESS_TOKEN)
    
    serving     = dkube_serving_op(model=train.outputs['artifact'], device='cpu',
                                    serving_image=json.dumps({"image": "ocdr/tensorflowserver:2.0.0"}),
                                    auth_token=DKUBE_ACCESS_TOKEN, min_replicas = '1',
                                    production="true").after(train)

print("Creating pipeline run")
#client.create_run_from_pipeline_func(xray_pipeline, run_name=pl_run_name, arguments={'token':DKUBE_ACCESS_TOKEN})

