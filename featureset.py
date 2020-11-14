import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from dkube.sdk import *

if __name__ == "__main__":

    user = 'osm'
    dkubeURL = 'https://172.16.146.128:32222'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9zbSIsInJvbGUiOiJkYXRhc2NpZW50aXN0LG1sZSxwZSxvcGVyYXRvciIsImV4cCI6NDg0MzM0MjEyNCwiaWF0IjoxNjAzMzQyMTI0LCJpc3MiOiJES3ViZSJ9.lPC2nKHLHOJx06yfiYuW29kqcUcrZYt2ikkwCYfkwicmi9CQPJDL0nDQQNylrqaIOFPnk0_ndZuecu934ijZWN-qSmU8Y1VpTi3StKja7_u3ZqHcg3irKZCjCruphPLKV51gMSfZ2Dwjm6Cw_ylwxHSgjySD5rQFsNIpWcqrY0qg8eIVYMmhegHwXo4Hs0nhfSGiYShcZhI81Dsts8D6oM_8ss8q1Uk4jlIyd_W1MQ1dJ8l9P0h3YYCFnxkkpwmblYpJofO0TCSCYQ-nOv7iptzkDjwvumW_X-1homIOxeUHppgNLV0BssT-IP3iM9zmhUEvSiZul7dg2OT8NMMJEA'

  
    '''
    training_name= generate('mnist')
    training = DkubeTraining(user, name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("python model.py")
    training.add_project("mnist")
    training.add_input_dataset("mnist", mountpath='/opt/dkube/input')
    training.add_output_model("mnist", mountpath='/opt/dkube/output')
    '''


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

    print(f"\n deleting featureset {featureset_name}")
    featuresets = []
    featuresets.append(featureset_name)
    response = api.delete_featureset(featuresets)
    print(response)


    #api.create_training_run(training)

