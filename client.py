import sys

sys.path.insert(0, '/home/dkube/ahmed/dkube-sdk/dkube')

from dkube.sdk.dkube import *
import os

if __name__ == "__main__":
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkIjoxNTc4Mzg4MjAyLCJyb2xlIjoib3BlcmF0b3IiLCJ1c2VybmFtZSI6Im9jIn0.uAStfXdrojBBE_vx8Uyow1Coj1lQdG3mAzGBWbF4z_0'
    env = Environment(scheme='https', host='34.83.166.110', user='oc', token=token, port=32222)
    
    launch_training_job("test", autogenerate=True, environ=env.external, 
            workspace='mnist-1', script='python model.py',
            datasets=['mnist'], models=['mnist'], template='test-7976809512')
    
    
    #export_model("/tmp/test-model", "test", autogenerate=True, environ=env.external, framework=Framework.Unknown)
