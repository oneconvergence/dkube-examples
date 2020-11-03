import sys
import os

#sys.path.insert(0, os.path.abspath('../'))

from dkube.sdk import *

if __name__ == "__main__":

    dkubeURL = ''
    authToken = ''

    '''
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
    training = DkubeTraining('mak-454', name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("python model.py")
    training.add_project("mnist")
    training.add_input_dataset("mnist", mountpath='/opt/dkube/input')
    training.add_output_model("mnist", mountpath='/opt/dkube/output')

    serving_name=geneirate('mnist')
    serving = DkubeServing('mak-454', name=serving_name, description='serving deployed from dkube sdk')
    serving.set_transformer(True, script='tensorflow/classification/mnist/digits/transformer/transformer.py')
    serving.update_serving_model("mnist")

    notebook_name= generate('mnist')
    notebook = DkubeIDE('mak-454', name=notebook_name, description='triggered from dkube sdk')
    notebook.update_container(framework="tensorflow_1.14", image_url="ocdr/dkube-datascience-rs-tf-cpu-multiuser:v1.14")

    publish_name=generate('mnist')
    publish_details = DkubeServing('mak-454', name=publish_name, description='model published from dkube sdk')
    publish_details.set_transformer(True, script='tensorflow/classification/mnist/digits/transformer/transformer.py')
    publish_details.update_serving_model("mnist", version='1604346481344')
	'''


    api = DkubeApi(URL=dkubeURL, token=authToken)
    #api.launch_jupyter_ide(notebook)
    #api.launch_rstudio_ide(notebook)
    #print(api.list_ides('mak-454'))
    #api.delete_ide('mak-454', 'mnist-4674')
    # api.create_project(project)
    # api.create_dataset(dataset)
    # api.create_model(model)
    #v = api.get_model_version("mak-454", "mnist", "1604347322339")
    #api.publish_model(publish_name, "publishing mnist model", publish_details)
    #api.release_model("mak-454", "mnist", "1604345493555")

    # api.create_training_run(training)

    #api.create_test_inference(serving)

    #lineage = api.get_model_lineage('mak-454', 'mnist', '1604322708542')
    #lineage = api.get_training_run_lineage('mak-454', 'mnist-4990')
    #versions = api.get_dataset_versions('mak-454', 'mnist')
    #versions = api.get_model_versions('mak-454', 'mnist')

    #version = api.get_model_latest_version('mak-454', 'mnist')
    #version = api.get_dataset_latest_version('mak-454', 'mnist')

    #cap = api.get_datascience_capabilities()
    #print(api.get_notebook_capabilities())
    #print(api.get_r_capabilities())
    #print(api.get_training_capabilities())
    print(api.get_serving_capabilities())

    '''
    reruns = api.trigger_runs_bydataset("mnist", "oc")
    import json
    print('List of reruns - {}'.format(json.dumps(reruns)))
    '''

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

