import sys

sys.path.insert(0, '/home/dkube/ahmed/dkube-sdk/dkube')

from dkube.sdk import *
import os

if __name__ == "__main__":
    token = ''
    conn = Connection()
    conn.scheme = 'https'
    conn.host = ''
    conn.port = 32222
    conn.token = token

    
    #project = ProjectRepo(source=Github('https://github.com/oneconvergence/dkube-examples/tree/2.0.5/tensorflow/classification/mnist/digits/classifier/program', '2.0.5'), name='mnist-2')
    #create_repo('administrator', project, conn=conn)

    #dataset = DatasetRepo(name='mnist', source=Github('https://github.com/kubeflow/kubeflow.git', 'master'))
    #create_repo('administrator', dataset, conn=conn)

    
    #model = ModelRepo(name='mnist')
    #create_repo('administrator', model, conn=conn)
    
    #list_versions('administrator', DatasetRepo(name='mnist'), conn=conn)
    #list_versions('administrator', ModelRepo(name='mnist'), conn=conn)

    #project = ProjectRef('mnist-2')
    #dataset = DatasetRef('mnist', mount='/opt/dkube/input')
    #model = ModelRef('mnist', mount='/opt/dkube/output')

    #run = Run()
    #run.add_script('python model.py')
    #run.add_input_project(project)
    #run.add_input_dataset(dataset)
    #run.add_output_model(model)

    #create_run('administrator', run, conn=conn)
    #get_run('oc', 'run-run-2199933074', conn=conn)
    #list_run('oc', conn=conn)
