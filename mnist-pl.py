import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler

from dkube.pipelines import *
from dkube.sdk import *

@dsl.pipeline(
    name='dkube-mnist-pl',
    description='sample mnist digits pipeline with dkube components'
)
def d3pipeline():
    token = 'eyJTZXNzaW9uIjp0cnVlLCJUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpqY21WaGRHVmtJam94TlRjd01qVTNNakE1TENKeWIyeGxJam9pYjNCbGNtRjBiM0lpTENKMWMyVnlibUZ0WlNJNkltOWpaR3QxWW1VaWZRLlBsYjZMNEhDME16ZDlPLTItS1hrQVdyVGRyV2xCaGM1bGEyVEhCWk1kejQifQ=='
    env = Environment(ip='192.168.200.19', user='ocdkube', token=token)

    train   = dkube_training_op(
            env=env, framework=Framework.Tensorflow, name='mnist-new', 
            container={'image':'docker.io/ocdr/dkube-datascience-tf-cpu:v1.14'},
            command='python model.py',
            envs={"steps": 100},
            program='mnist',
            datasets=['mnist'])

compiler.Compiler().compile(d3pipeline, 'dkube_mnist_pl.tar.gz')
