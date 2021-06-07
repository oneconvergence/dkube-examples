import kfp
from kubernetes.client import V1Toleration

@kfp.dsl.pipeline(
    name='Parallel stages pipeline',
    description='An example pipeline to launch number of stages in parallel'
)
def parallel_pipeline():
    count = 22
    for i in range(count):
        op = kfp.dsl.ContainerOp(name='parallel',image="alpine",command=["sleep", "5s"])
        op.add_toleration(V1Toleration( effect='NoSchedule', key='node.kubernetes.io/unschedulable', operator='Exists'))
