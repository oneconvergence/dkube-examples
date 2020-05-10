import sys

from dkube.sdk import *
from dkube.sdk.lib.api import *

if __name__ == "__main__":

    dkubeURL = 'https://192.168.200.106:32222'
    authToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc0YmNkZjBmZWJmNDRiOGRhZGQxZWIyOGM2MjhkYWYxIn0.eyJ1c2VybmFtZSI6Im9jIiwicm9sZSI6Im9wZXJhdG9yIiwiaWF0IjoxNTg3NzIxNTE4LCJpc3MiOiJES3ViZSJ9.OQmeuygUqH9qPSUm-SrqeyTdekMOH0E3XBeaCYLSmEh-oRXRL3XhEtLnHhXn6KPzXWkEuDo1W_FyrUEpXZsXXHP-Fjt1cF08IXmSxWIRRw9-dcAuPJxBzgmxyJWpTVlSiwN8HhfJNuTPk8sSUhzPLmBD4eEN3gGS3FP7_VdvXDOpgYW7__IkN7qpfkdz6H0mMeAcsazDbZ1ZwMoVkBq-Ad6UnQ-5FvfWYxVPPKD95QGmpGz7TpAmbYHMFWTWIgyxuQnw24W72wn1Un21C1P9HUTSIPLQHqO6sbhHaZVmWGdzcMN1wmGSWqJucKyQHUCntVyx0axDMDbXSnuwNuBWaQ'


    project_name = generate('mnist')
    project = DkubeProject('oc', name=project_name)
    project.update_project_source(source='github')
    project.update_github_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/program', branch='2.0.6')
    

    dataset_name = generate('mnist')
    dataset = DkubeDataset('oc', name=dataset_name)
    dataset.update_dataset_source(source='github')
    dataset.update_github_details('https://github.com/oneconvergence/dkube-examples/tree/2.0.6/tensorflow/classification/mnist/digits/classifier/data', branch='2.0.6')

    model_name = generate('mnist')
    model = DkubeModel('oc', name=model_name)
    model.update_model_source(source='dvs')


    training_name= generate('mnist')
    training = DkubeTraining('oc', name=training_name)
    training.add_project(project_name)
    training.add_input_dataset(dataset_name, mountpath='/opt/dkube/input')
    training.add_output_model(model_name, mountpath='/opt/dkube/output')


    api = DkubeApi(dkubeURL=dkubeURL, authToken=authToken)
    #api.create_project(project)
    #api.create_dataset(dataset)
    #api.create_model(model)

    #Bug - getting fixed in 2.0.8, it takes little time to reflect version even after datum state is ready
    #time.sleep(30)

    #api.create_training_run(training)

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
