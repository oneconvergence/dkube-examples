import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from dkube.sdk import *

if __name__ == "__main__":

    user = 'osm'
    dkubeURL = 'https://172.16.146.128:32222'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9zbSIsInJvbGUiOiJkYXRhc2NpZW50aXN0LG1sZSxwZSxvcGVyYXRvciIsImV4cCI6NDg0NTQwNjcxNywiaWF0IjoxNjA1NDA2NzE3LCJpc3MiOiJES3ViZSJ9.0sb9UTU8DDv42Wml4GQP6tdTPLOpkHbED8aw-cRf1uGBKfW7cD5TNNVckkVAEYgwZrpdBeDFj3vnhn_GLJMjxzC9rDlaIE50Aka1OLOiaN5_qvpBbKdTqiIglFLmIZSj9mESCfnqQtP2o2FKdJHdJo6Zeawb5-IBFZu3dMIgrdDtPlIwV40ICqUjH5S-3D0UtaEkcNRyO0h2BGbhro8jHfX88MYYmMurXhRJs2BgnvP_6Or0_mheuBsClTXbM3m62Oc2Mqml0gk23_qEqdmcPv3i9wF0tS3AM4vTVbN-gV7SrLaRph93mntD6NFv9AX7wcVIs1qxY1DfsstvRPYawQ'

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
    print(f"\n deleting featureset {featureset_name}")
    featuresets = []
    featuresets.append(featureset_name)
    response = api.delete_featureset(featuresets)
    print(response)
    """

    dataset_name = generate('mnist')
    dataset = DkubeDataset(user, name=dataset_name)
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/data', branch='2.0.6')
    
    api.create_dataset(dataset)
    # Preprocessing run
    preprocess_name= generate('mnist-preprocess')
    preprocess = DkubePreprocessing(user, name=preprocess_name, description='triggered from dkube sdk')
    preprocess.update_container(image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    preprocess.update_startupscript("sleep 2000")
    #preprocess.add_project("mnist")
    preprocess.add_input_dataset("mnist", mountpath='/opt/dkube/input')
    preprocess.add_output_featureset(featureset_name, mountpath='/opt/dkube/output')

    api.create_preprocessing_run(preprocess)

    '''
    training_name= generate('mnist')
    training = DkubeTraining(user, name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("python model.py")
    training.add_project("mnist")
    training.add_input_dataset("mnist", mountpath='/opt/dkube/input')
    training.add_output_model("mnist", mountpath='/opt/dkube/output')
    '''

    #api.create_training_run(training)

