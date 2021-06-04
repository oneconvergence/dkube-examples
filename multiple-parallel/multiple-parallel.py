import kfp
import json,os

from dkube.pipelines import *


@kfp.dsl.pipeline(
    name='Parallel stages pipeline',
    description='An example pipeline to launch number of stages in parallel'
)
def parallel_pipeline():
    count = 22
    for i in range(count):
        op = kfp.dsl.ContainerOp(name='parallel',
            image="ocdr/d3-datascience-tf-cpu:v1.14",
            command=["sleep", "5s"])
        op.add_toleration(V1Toleration( effect='NoSchedule', key='node.kubernetes.io/unschedulable', operator='Exist))
