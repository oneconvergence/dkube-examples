import sys
import os

sys.path.insert(0, os.path.abspath('../'))

from dkube.sdk import *

if __name__ == "__main__":

    dkubeURL = 'https://35.227.115.171:32222'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9jIiwicm9sZSI6Im9wZXJhdG9yIiwiZXhwIjo0ODQxNDQ3MDM1LCJpYXQiOjE2MDE0NDcwMzUsImlzcyI6IkRLdWJlIn0.vIV2-dip23yCUumh3auNNSjXETRa2_NqJgUPyrP1-dIqd3OvDvmWKTIFTser1ycoIpPM4hXDDJxcyiDU3JA5pFkbT0m0Y4V8sT4cQQUpjyIO5mRGvfZYha5vb_-Kw7CLZMpRKmbgxOy7tdZcywlXLqLmItrYjmZWeEvvQPzkKASl9O5d5dsQvx3LZ3bT4Gp1Fps-x0wl0n7G_pY9wQJKIqWvWjoa8tKVVYlnmYBTmne3jguYaGv_dkIDVi7AK2bAJ-_3u9NQnYQS1-oevVfdHu8kfH0fVoxOyOjMWZw2I7gPRHmndR2mhB9EzCsrFUlGzS2SDvoBQ2v0bvHau3vyqA'


    '''
    project_name = generate('mnist')
    project = DkubeProject('oc', name=project_name)
    project.update_git_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program', branch='2.0.6')
    '''
    

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

    serving_name=generate('mnist')
    serving = DkubeServing('oc', name=serving_name, description='serving deployed from dkube sdk')
    serving.update_transformer_code(project='mnist', code='transformer.py')
    serving.update_transformer_image(image_url='ocdr/d3-datascience-tf-cpu:v1.14')
    serving.update_serving_model("mnist", version="1601882977956")
    serving.update_serving_image(image_url='ocdr/d3-datascience-tf-cpu:v1.14')


    api = DkubeApi(URL=dkubeURL, token=authToken)
    #api.create_project(project)
    #api.create_dataset(dataset)
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
