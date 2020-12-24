import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler

from dkube.sdk import *
from dkube.pipelines import *

def dkube_mnist_pipeline(
        user=None,
        authtoken=None,
        code=None,
        dataset=None,
        model=None,
        nworkers=0,
        ngpus=0):

    training_name= generate('mnist')
    training = DkubeTraining(str(user), name=training_name, description='triggered from dkube pl launcher')
    training.update_container(framework="tensorflow_1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript('python model.py')
    training.add_project(str(code))
    training.add_input_dataset(str(dataset), mountpath='/opt/dkube/input')
    training.add_output_model(str(model), mountpath='/opt/dkube/output')

    training_op = dkube_training_op(
                name='mnist-training',
                authtoken=authtoken,
                training=training)

    serving_name = generate('mnist')
    serving = DkubeServing(str(user), name=serving_name, description='triggered from dkube pl launcher')
    serving.set_transformer(True, script='tensorflow/classification/mnist/digits/transformer/transformer.py')
    serving.update_serving_model(str(model))

    serving_op = dkube_serving_op(
            name='mnist-serving',
            authtoken=authtoken,
            serving=serving).after(training_op)

compiler.Compiler().compile(dkube_mnist_pipeline, 'dkube_mnist_pl.tar.gz')
