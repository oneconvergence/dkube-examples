import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler

from dkube.sdk import *
from dkube.pipelines import *

@dsl.pipeline(
    name='dkube_mnist_pl',
    description='sample mnist digits pipeline with dkube components'
)
def dkube_mnist_pipeline(
		authtoken=None,
		project=None,
		dataset=None,
		model=None,
		script='python model.py',
		nworkers=0,
		ngpus=0):

    training_name= generate('mnist')
    training = DkubeTraining('mak-454', name=training_name, description='triggered from dkube pl launcher')
    training.update_container(framework="tensorflow_v1.14", image_url="ocdr/d3-datascience-tf-cpu:v1.14")
    training.update_startupscript(str(script))
    training.add_project(str(project))
    training.add_input_dataset(str(dataset), mountpath='/opt/dkube/input')
    training.add_output_model(str(model), mountpath='/opt/dkube/output')

    training_op = dkube_training_op(
	            name='mnist-training',
				authtoken=authtoken,
				training=training)

compiler.Compiler().compile(dkube_mnist_pipeline, 'dkube_mnist_pl.tar.gz')
