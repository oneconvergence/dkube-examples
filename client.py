import sys

sys.path.insert(0, '/home/dkube/sdk/dkube/')

from dkube.sdk.dkube import *
import os

if __name__ == "__main__":
    token = 'eyJTZXNzaW9uIjp0cnVlLCJUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpqY21WaGRHVmtJam94TlRjek1EVXdNVFV6TENKeWIyeGxJam9pYjNCbGNtRjBiM0lpTENKMWMyVnlibUZ0WlNJNkltOWpaR3QxWW1VaWZRLlBGRFJTcC1UbXJNeUJRMXRLWm1EX0FmaHFCMVVOZkYtQW9wbjBVTjVFUXcifQ=='
    env = Environment(scheme='https', host='18.236.126.102', user='ocdkube', token=token, port=32222)
    launch_training_job("test", autogenerate=True, environ=env.external, 
            workspace='mnist', script='python model.py',
            datasets=['mnist'])
    #export_model("/tmp/test-model", "test", autogenerate=True, environ=env.external, framework=Framework.Unknown)
