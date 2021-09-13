import kubernetes
from kfp import components, dsl

@dsl.python_component(name, base_image)
def print_secret(user):
    '''Displays access-token secret'''
    from kubernetes import client, config
    config.load_incluster_config()
    v1=client.CoreV1Api()
    
    print(v1.read_namespaced_secret("access-token", user))

print_secret_op = components.func_to_container_op(
    print_secret,
    base_image="chris060986/python-kube-client:latest", 
)

@dsl.pipeline(
    name='volumes_and_secret',
    description='sample pipeline to display usage of volume and secrets'
)
def volumes_and_secret(username):
    """ Default storage class must be available in the cluster for pipelineVolume to work."""
    volume = dsl.PipelineVolume(volume=kubernetes.client.V1Volume(
        name=f"test-storage",
        empty_dir=kubernetes.client.V1EmptyDirVolumeSource()))
    print_volume = dsl.ContainerOp(name="print_volume", image="bash:latest", command=['df', '-h']).add_pvolumes({"/tmp": volume})
    _ = print_secret_op(str(username)).after(print_volume)
