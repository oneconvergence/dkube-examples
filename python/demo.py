import os
import sys

from dkube.sdk import *

#sys.path.insert(0, os.path.abspath('../'))


if __name__ == "__main__":

    authToken = os.getenv('DKUBE_USER_ACCESS_TOKEN')
    user = os.getenv('USERNAME', 'oc')

    code_name = generate('mnist')
    code = DkubeCode(user, name=code_name)
    code.update_git_details('https://github.com/oneconvergence/dkubeio-examples/tree/master/tf/classification/mnist/digits/classifier/program')

    dataset_name = generate('mnist')
    dataset = DkubeDataset(user, name=dataset_name)
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkubeio-examples-data/tree/master/tf/mnist')

    model_name = generate('mnist')
    model = DkubeModel(user, name=model_name)
    model.update_model_source(source='dvs')
    
    training_name= generate('mnist')
    training = DkubeTraining(user, name=training_name, description='triggered from dkube sdk')
    training.update_container(framework="tensorflow_1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript("python model.py")
    training.add_code("mnist")
    training.add_input_dataset("mnist", mountpath='/opt/dkube/input')
    training.add_output_model("mnist", mountpath='/opt/dkube/output')

    serving_name=geneirate('mnist')
    serving = DkubeServing(user, name=serving_name, description='serving deployed from dkube sdk')
    serving.set_transformer(True, script='tensorflow/classification/mnist/digits/transformer/transformer.py')
    serving.update_serving_model("mnist")

    notebook_name= generate('mnist')
    notebook = DkubeIDE(user, name=notebook_name, description='triggered from dkube sdk')
    notebook.update_container(framework="tensorflow_1.14", image_url="ocdr/dkube-datascience-rs-tf-cpu-multiuser:v1.14")

    publish_name=generate('mnist')
    publish_details = DkubeServing(user, name=publish_name, description='model published from dkube sdk')
    publish_details.set_transformer(True, script='tensorflow/classification/mnist/digits/transformer/transformer.py')
    publish_details.update_serving_model("mnist", version='1604346481344')


#     api = DkubeApi(token=authToken)
#     api.launch_jupyter_ide(notebook)
#     api.launch_rstudio_ide(notebook)
#     print(api.list_ides(user))
#     api.delete_ide(user, 'mnist-4674')
#     api.create_code(code)
#     api.create_dataset(dataset)
#     api.create_model(model)
#     v = api.get_model_version(user, "mnist", "1604347322339")
#     api.publish_model(publish_name, "publishing mnist model", publish_details)
#     api.release_model(user, "mnist", "1604345493555")

#     mc = api.modelcatalog(user)
#     item = api.get_modelcatalog_item(user, 'mnist-7206', '1606471424577')
#     api.create_model_deployment(user, 'dep1', 'mnist-7206', '1606471424577', stage_or_deploy='deploy')
#     api.delete_model_deployment(user, 'dep1')
#     deps = api.list_model_deployments(user)

#     api.create_training_run(training)

#     api.create_test_inference(serving)

#     lineage = api.get_model_lineage(user, 'mnist', '1604322708542')
#     lineage = api.get_training_run_lineage(user, 'mnist-4990')
#     versions = api.get_dataset_versions(user, 'mnist')
#     versions = api.get_model_versions(user, 'mnist')

#     version = api.get_model_latest_version(user, 'mnist')
#     version = api.get_dataset_latest_version(user, 'mnist')

#     cap = api.get_datascience_capabilities()
#     print(api.get_notebook_capabilities())
#     print(api.get_r_capabilities())
#     print(api.get_training_capabilities())
#     print(api.get_serving_capabilities())

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

