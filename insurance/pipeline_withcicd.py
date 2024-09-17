#!/usr/bin/env python
# coding: utf-8

# # Automating DKube Training and Serving with Kubeflow Pipelines
# 
# This notebook demonstrates how to automate DKube training and serving workflows using Kubeflow Pipelines.
# 
# DKube extends Kubeflow components by implementing specialized operators that integrate with the KFP SDK, providing a seamless interface for submitting components to the DKube platform.
# 
# DKube supports KFP components for various tasks, including training, serving, and preprocessing.

# In[ ]:


import json
import os
import kfp
from kfp import components
from dkube.sdk.api import DkubeApi
import random, string
from termcolor import colored


# In[ ]:


dkube_training_op = components.load_component_from_file("/mnt/dkube/pipeline/components/training/component.yaml")
dkube_serving_op  = components.load_component_from_file("/mnt/dkube/pipeline/components/serving/component.yaml")


# In[ ]:


## These fields must be modified to allow the file to run based on your repo names
## After the files are modified, run all of the cells to execute

training_program = "insurance" # Change this to identify your Code Repo name
training_dataset = 'insurance-dataset' # Change this to identify your Dataset Repo name
training_model = 'insurance-model' # Change this to identify your Model Repo name


# In[ ]:


## These fields are specific to this example, and should not be modified

image = "ocdr/dkube-datascience-tf-cpu:v2.6.0-19"
serving_image = "ocdr/tensorflowserver:2.6.0"
training_script = "python insurance/training.py"
transformer_code='insurance/transformer.py'
user = os.getenv('USERNAME')
framework = "tensorflow"
f_version = "2.6.0"
input_mount_point = "/opt/dkube/in"
output_mount_point = "/opt/dkube/out"


# In[ ]:


@kfp.dsl.pipeline(
    name='dkube-insurance-pl',
    description='sample insurance pipeline'
)
def insurance_pipeline(token, code=training_program, dataset=training_dataset,
                       model=training_model, deployment_name="insurance"):
    
    train       = dkube_training_op(token, json.dumps({"image": image}),
                                    framework=framework, version=f_version,
                                    program=code, run_script=training_script,
                                    datasets=json.dumps([str(dataset)]),
                                    input_dataset_mounts=json.dumps([input_mount_point]),
                                    outputs=json.dumps([str(model)]),
                                    output_mounts=json.dumps([output_mount_point]))
    
    serving     = dkube_serving_op(token, train.outputs['artifact'], device='cpu', 
                                    name=deployment_name,
                                    serving_image=json.dumps({"image": serving_image}),
                                    transformer_image=json.dumps({"image": image}),
                                    transformer_project=code,
                                    transformer_code=transformer_code,
                                    min_replicas="1").after(train)


# ## Create a run

# In[ ]:


token = os.getenv("DKUBE_USER_ACCESS_TOKEN")
api = DkubeApi(token=token)


# In[ ]:


res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

run_name = f"Insurance Run {res}"
experiment = "default"
deployment_name = f"{os.getenv('DKUBE_USER_LOGIN_NAME')}-{res}"


# In[ ]:


deployment_id = api.get_deployment_id(name=deployment_name)
if not deployment_id:
    print(f"On pipeline completion the deployment {colored(deployment_name, 'green', attrs=['bold'])} will be created")
    
    client = kfp.Client(existing_token=token)
    client.create_run_from_pipeline_func(insurance_pipeline, run_name=run_name, experiment_name=experiment,
                                         arguments={"token":token, "deployment_name":deployment_name}
                                        )
    pl_config = {"DEPLOYMENT_NAME":deployment_name}
    get_ipython().run_line_magic('store', 'pl_config')

else:
    print("Deployment Already Existing, skipping create, try running the cells again")

