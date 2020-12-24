import os
import sys

from dkube.sdk import *

sys.path.insert(0, os.path.abspath('../'))

def _create_featureset_specfiles(spec1_path, spec2_path):

    # spec1 metadata
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
    open(spec1_path, "w").write(features_metadata)

    features_metadata = """- name: Customer Name
  description: Customer Name
  schema: string
- name: Gender
  description: Gender
  schema: string
- name: Company
  description: Company affiliation
  schema: string
- name: Units
  description: Number of DKube licenses
  schema: int64
- name: revenue
  description: Total revenue
  schema: int64
"""
    open(spec2_path, "w").write(features_metadata)


if __name__ == "__main__":

    user = os.getenv('USERNAME')
    dkubeURL = 'https://172.16.146.128:32222'
    authToken = os.getenv('DKUBE_USER_ACCESS_TOKEN')

    spec1_path = "/tmp/spec1.yaml"
    spec2_path = "/tmp/spec2.yaml"
    _create_featureset_specfiles(spec1_path, spec2_path)

    featureset_name = generate('featureset-2020')
    print(f"Featureset name {featureset_name}\n")

    featureset = DkubeFeatureSet(name=featureset_name, description="FeatureSet experiments", tags=[
                                 "pandemic:covid", "war:none"])
    featureset.update_featurespec_file(spec1_path)
    print(f"---- Featureset name {featureset_name} -- Create featureset \n")

    api = DkubeApi(URL=dkubeURL, token=authToken)
    api.create_featureset(featureset)

    print(f"---- Featureset name {featureset_name} -- uploading new spec file \n")
    api.upload_featurespec(featureset_name, spec2_path)

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

    # Create a code

    
    code_name = generate('mnist')
    code = DkubeCode(user, name=code_name)
    code.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program', branch='2.0.6')

    api.create_code(code)
    
    # Create model repo

    model_name = generate('mnist')
    model = DkubeModel(user, name=model_name)
    model.update_model_source(source='dvs')

    api.create_model(model)

    """

    """
    # Preprocessing run
    code_name = "mnist-fs"
    dataset_name = "mnist-fs"
    featureset_name = "A"
    preprocess_name = generate('mnist-fs')
    preprocess = DkubePreprocessing(
        user, name=preprocess_name, description='triggered from dkube sdk')
    preprocess.update_container(image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    preprocess.update_startupscript("sleep 200000")
    preprocess.add_code(code_name)
    preprocess.add_input_dataset(dataset_name, mountpath='/opt/dkube/input')
    preprocess.add_output_featureset(
        featureset_name, mountpath='/opt/dkube/output')

    api.create_preprocessing_run(preprocess)
    
    
    training_name= generate('mnist')
    training = DkubeTraining(user, name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    #training.update_startupscript("python model.py")
    training.update_startupscript("sleep 1000")
    training.add_code(code_name)
    training.add_input_dataset(dataset_name, mountpath='/opt/dkube/input')
    training.add_output_model(model_name, mountpath='/opt/dkube/output')
    training.add_input_featureset(featureset_name, mountpath='/opt/dkube/featureset')
    

    api.create_training_run(training)
    """
