import kubernetes
from kfp import components, dsl

@dsl.python_component(
    name='print_secret_op',
    base_image="ocdr/dkube-datascience-tf-cpu:v2.0.0-6" 
)
def print_secret(user):
    '''Calculates sum of two arguments'''
    from kubernetes import client, config
    config.load_incluster_config()
    v1=client.CoreV1Api()
    
    print(v1.read_namespaced_secret("access-token", user))

print_secret_op = components.func_to_container_op(
    print_secret,
    base_image="ocdr/dkube-datascience-tf-cpu:v2.0.0-6", 
)

@dsl.pipeline(
    name='volumes_and_secret',
    description='sample pipeline to display usage of volume and secrets'
)
def volumes_and_secret(username):
    volume = dsl.PipelineVolume(volume=kubernetes.client.V1Volume(
        name=f"test-storage",
        empty_dir=kubernetes.client.V1EmptyDirVolumeSource()))
    mount_folder = "/tmp"
    print_secret = print_secret_op(str(username)).add_pvolumes({mount_folder: volume})
    _ = dsl.ContainerOp(name="print_volume", image="bash:latest", command=['df', '-h']).add_pvolumes({mount_folder: volume}).after(print_secret)