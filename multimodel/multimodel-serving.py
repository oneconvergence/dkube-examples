### Importing libraries
import os,sys,kfp,zipfile,json
from dkube.sdk import *

### Dkube-SDK
token = os.getenv("DKUBE_USER_ACCESS_TOKEN")
username =  os.getenv("USERNAME")
dkube_url = os.getenv("DKUBE_URL")
api = DkubeApi(URL=dkube_url,token=token)

### Creating model
model = DkubeModel(username, name="multimodel")
model.update_model_source(source="git")
model.update_git_details(url="https://github.com/mak-454/dkubeio-examples/blob/multimodel/R/classification/multimodel/models.zip")
api.create_model(model)

### Extracting model
def extract_model():
    model_versions = api.get_model_versions(username,"multimodel")
    model_version = model_versions[0]['version']['uuid'] 
    path_to_zip_file = "/home/"+username+"/model/multimodel/"+model_version+"/data/models.zip"
    model_artifacts = "/home/"+username+"/model/multimodel/"+ model_version +"/data/models/"
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(model_artifacts)
        
extract_model()

### Pipeline Components
search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_serving_op = component_store.load_component("serving")

### Pipeline Definition

@kfp.dsl.pipeline(
    name='multimodel-pl',
    description='multimodel pipeline'
)
def multimodel_pipeline(token):
    
        serving     = dkube_serving_op(token, model = "multimodel" , device='cpu', serving_image='{"image":"ocdr/inf-multimodel:latest"}')
