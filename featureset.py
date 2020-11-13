import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from dkube.sdk import *

if __name__ == "__main__":

    dkubeURL = 'https://172.16.146.128:32222'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9zbSIsInJvbGUiOiJkYXRhc2NpZW50aXN0LG1sZSxwZSxvcGVyYXRvciIsImV4cCI6NDg0MzM0MjEyNCwiaWF0IjoxNjAzMzQyMTI0LCJpc3MiOiJES3ViZSJ9.lPC2nKHLHOJx06yfiYuW29kqcUcrZYt2ikkwCYfkwicmi9CQPJDL0nDQQNylrqaIOFPnk0_ndZuecu934ijZWN-qSmU8Y1VpTi3StKja7_u3ZqHcg3irKZCjCruphPLKV51gMSfZ2Dwjm6Cw_ylwxHSgjySD5rQFsNIpWcqrY0qg8eIVYMmhegHwXo4Hs0nhfSGiYShcZhI81Dsts8D6oM_8ss8q1Uk4jlIyd_W1MQ1dJ8l9P0h3YYCFnxkkpwmblYpJofO0TCSCYQ-nOv7iptzkDjwvumW_X-1homIOxeUHppgNLV0BssT-IP3iM9zmhUEvSiZul7dg2OT8NMMJEA'


    project_name = generate('mnist')
    project = DkubeProject('oc', name=project_name)
    project.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program', branch='2.0.6')
    

    dataset_name = generate('mnist')
    dataset = DkubeDataset('oc', name=dataset_name)
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/data', branch='2.0.6')

    model_name = generate('mnist')
    model = DkubeModel('oc', name=model_name)
    model.update_model_source(source='dvs')


    
    training_name= generate('mnist')
    training = DkubeTraining('oc', name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("python model.py")
    training.add_project("mnist")
    training.add_input_dataset("mnist", mountpath='/opt/dkube/input')
    training.add_output_model("mnist", mountpath='/opt/dkube/output')


    """
    serving_name=generate('mnist')
    serving = DkubeServing('oc', name=serving_name, description='serving deployed from dkube sdk')
    serving.update_transformer_code(project='mnist', code='transformer.py')
    serving.update_transformer_image(image_url='ocdr/d3-datascience-tf-cpu:v1.14')
    serving.update_serving_model("mnist", version="1601882977956")
    serving.update_serving_image(image_url='ocdr/d3-datascience-tf-cpu:v1.14')
    """

    featureset_name = generate('elections-2020')
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

    api.list_datasets

    apu.create_project(project)
    api.create_dataset(dataset)
    #api.create_model(model)

    #api.create_training_run(training)

    #api.create_test_inference(serving)

    reruns = api.trigger_runs_bydataset("mnist", "oc")
    import json
    print('List of reruns - {}'.format(json.dumps(reruns)))

    '''
    training_name = 'pltraining-3500'
    outputs = api.get_training_outputs('oc', training_name)

    artifacts = [
                    {'datum': output['version']['datum_name'], 'class': output['version']['datum_type'],
                     'version': output['version']['uuid'], 'index': output['version']['index']
                    }
                    for output in outputs
                ]

    import json
    print('{}'.format(json.dumps(artifacts)))

    model_type = outputs[0]['version']['datum_type']
    model_name = outputs[0]['version']['datum_name']
    version = outputs[0]['version']['uuid']
    index = outputs[0]['version']['index']

    print('Generated version - {} for model {} at index {}'.format(version, model_name, index))
    '''
