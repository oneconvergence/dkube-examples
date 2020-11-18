import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from dkube.sdk import *

if __name__ == "__main__":

    user = 'osm'
    dkubeURL = 'https://172.16.146.128:32222'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9zbSIsInJvbGUiOiJkYXRhc2NpZW50aXN0LG1sZSxwZSxvcGVyYXRvciIsImV4cCI6NDg0NTY0NDMyMywiaWF0IjoxNjA1NjQ0MzIzLCJpc3MiOiJES3ViZSJ9.xMd-OpVe4-RdVClyvzX4bhibWNNB4nDI9WY4qbMGyYyJzrUMjb4xa-6hf0EbOXUh7ePYjKwFyuJJa-tXTj-L_pF_QlyycKF66WPIAl6-soMFIhmZXWlGCUqXHF9-pUkBqlpLLCwz07Z4nUzksMPkoIbHwWf_MUNll-lbaCNgd-z_X97ADu6lTBfhm3bV2eXnDBV5oBoxjF0Fg4fJxl_dNBzw926lswaWwndElr3VyDtpxV5hcsVKFFufunIn6r4leP6K_fYnT6E449IWOaAxYoxyTkmhQDkHBAJ3Odpd19wry1xgi9erRHB059oSr8wP3JqcPqP6hRTdpIEA9id03g'

    featureset_name = generate('elections-2020')
    print(f"Featureset name {featureset_name}")

    featureset = DkubeFeatureSet(name=featureset_name, description="Elections 2020 analysis", tags=["pandemic:covid", "war:none"])
    # Update specfile location
    features_metadata = """- name: Name
  description: Presidential candidate name
  schema: string
- name: age
  description: Age
  schema: int
- name: Gender
  description: Gender
  schema: string
- name: Party
  description: Party affiliation
  schema: string
- name: Popular vote
  description: Total votes 
  schema: int
- name: electoral votes
  description: Total electoral votes
  schema: int
- name: winner
  description: is he the winner
  schema: boolean
"""
    open("/tmp/spec-biden.yaml", "w").write(features_metadata)
    featureset.update_featurespec_file("/tmp/spec-biden.yaml")

    api = DkubeApi(URL=dkubeURL, token=authToken)
    api.create_featureset(featureset)

    response = api.list_featuresets()
    print("\nfeatureset lists\n")
    print(response)

    """
    # Delete a featureset

    print(f"\n deleting featureset {featureset_name}")
    featuresets = []
    featuresets.append(featureset_name)
    response = api.delete_featureset(featuresets)
    print(response)
    """

    """
    # Create a dataset

    dataset_name = generate('mnist')
    dataset = DkubeDataset(user, name=dataset_name)
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/data', branch='2.0.6')

    api.create_dataset(dataset)

    # Create a project

    
    project_name = generate('mnist')
    project = DkubeProject(user, name=project_name)
    project.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program', branch='2.0.6')

    api.create_project(project)
    
    # Create model repo

    model_name = generate('mnist')
    model = DkubeModel(user, name=model_name)
    model.update_model_source(source='dvs')

    api.create_model(model)

    """
    # Preprocessing run
    project_name = "mnist-fs"
    dataset_name = "mnist-fs"
    featureset_name = "A"
    preprocess_name= generate('mnist-fs')
    preprocess = DkubePreprocessing(user, name=preprocess_name, description='triggered from dkube sdk')
    preprocess.update_container(image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    preprocess.update_startupscript("sleep 200000")
    preprocess.add_project(project_name)
    preprocess.add_input_dataset(dataset_name, mountpath='/opt/dkube/input')
    preprocess.add_output_featureset(featureset_name, mountpath='/opt/dkube/output')

    api.create_preprocessing_run(preprocess)
    """
    
    training_name= generate('mnist')
    training = DkubeTraining(user, name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    #training.update_startupscript("python model.py")
    training.update_startupscript("sleep 1000")
    training.add_project(project_name)
    training.add_input_dataset(dataset_name, mountpath='/opt/dkube/input')
    training.add_output_model(model_name, mountpath='/opt/dkube/output')
    training.add_input_featureset(featureset_name, mountpath='/opt/dkube/featureset')
    

    api.create_training_run(training)
    """
