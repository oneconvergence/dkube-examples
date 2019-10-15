import kfp.dsl as dsl
from kfp import components
import kfp.compiler as compiler

import sys
sys.path.insert(0, '/home/dkube/ahmed/oc-dkube-sdk/dkube/')

from dkube.sdk.dkube import *
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
            env=env.external, name='mnist-new', 
            container=ContainerImage.DKUBE_DS_TF_CPU_1_14,
            script='python model.py',
            envs={'steps': 100, 'batchsize': 100},
            program='mnist',
            datasets=['mnist'])

compiler.Compiler().compile(d3pipeline, 'dkube_mnist_pl.tar.gz')
