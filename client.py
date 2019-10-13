import sys

sys.path.insert(0, '/home/dkube/ahmed/oc-dkube-sdk/dkube/')

from dkube.sdk.dkube import *
import os

if __name__ == "__main__":
    token = 'eyJTZXNzaW9uIjp0cnVlLCJUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpqY21WaGRHVmtJam94TlRjd01qVTNNakE1TENKeWIyeGxJam9pYjNCbGNtRjBiM0lpTENKMWMyVnlibUZ0WlNJNkltOWpaR3QxWW1VaWZRLlBsYjZMNEhDME16ZDlPLTItS1hrQVdyVGRyV2xCaGM1bGEyVEhCWk1kejQifQ=='
    env = Environment(ip='192.168.200.19', user='ocdkube', token=token)
    launch_training_job("test", autogenerate=True, environ=env.external, 
            framework=Framework.Tensorflow, workspace='mnist', script='python model.py',
            datasets=['mnist'])
    #export_model("/tmp/test-model", "test", autogenerate=True, environ=env.external, framework=Framework.Unknown)
