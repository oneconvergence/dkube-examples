import os
import requests
import fire
from huggingface_hub import snapshot_download
from dkube.sdk import *

# This program runs only inside dkube notebook
def download_add_version(dkube_model, hf_repo_id):
    authToken = os.getenv('DKUBE_USER_ACCESS_TOKEN', '')
    user = os.getenv('USERNAME', 'oc')
    headers = {"Authorization": "Bearer " + authToken}
    url = "http://dkube-controller-master.dkube:5000/dkube/v2/controller/users/{}/datum/model/{}/addversion".format(user, dkube_model)
    model = {"name": dkube_model,"class": "model","remote": "false","source": "dvs"}
    resp = requests.post(url, json=model, headers=headers)
    resp.raise_for_status()
    ver_id = resp.json()["data"]["version"]["uuid"]
    api = DkubeApi(token=authToken)
    ver = api.get_model_version(user, dkube_model, ver_id)
    local_dir = os.path.join(os.getenv("HOME"), "model", ver["datum_name"], ver_id, "data")
    snapshot_download(repo_id=hf_repo_id, local_dir=local_dir, local_dir_use_symlinks=False)
    print("Created new version in dkube model={}, version index={}, version uid={}".format(dkube_model, ver["name"], ver_id))

if __name__ == "__main__":
    fire.Fire(download_add_version)
