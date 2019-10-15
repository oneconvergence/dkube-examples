import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler

from dkube.sdk.dkube import *
from dkube.pipelines import *
from dkube.sdk import *

@dsl.pipeline(
    name='dkube_mnist_pipeline',
    description='sample mnist digits pipeline with dkube components'
)
def dkube_mnist_pipeline(container=ContainerImage.DKUBE_DS_TF_CPU_1_14.value.to_dict(),
        token=os.getenv("DKUBE_USER_ACCESS_TOKEN"),
        program='mnist',
        dataset=['mnist'],
        envs=[{"steps": 100, "batchsize": 100}],
        hptuning={},
        ngpus=0):

    env = Environment(token='%s'%(token))

    train   = dkube_training_op(
            env=env.external, name='mnist-new', 
            container=container,
            script='python model.py',
            envs=envs,
            program=program,
            datasets=dataset,
            ngpus=ngpus)

compiler.Compiler().compile(dkube_mnist_pipeline, 'dkube_mnist_pipeline.tar.gz')
