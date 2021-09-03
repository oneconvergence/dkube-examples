import kfp

@kfp.dsl.pipeline(
    name='Parallel stages pipeline',
    description='An example pipeline to launch number of stages in parallel'
)
def parallel_pipeline():
    for i in range(22):
        op = kfp.dsl.ContainerOp(name='parallel',image="alpine",command=["sleep", "5s"])
