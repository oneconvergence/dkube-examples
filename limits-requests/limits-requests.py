import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_training_op = component_store.load_component("training")


@kfp.dsl.pipeline(name="set-envvars-pl", description="pl with limits and requests ")
def limits_requests_pipeline(
    code, run_script, limit_cpu, limit_memory, request_cpu, request_memory, token
):

    a = [
        {"LIMIT_CPU": str(limit_cpu)},
        {"LIMIT_MEM": str(limit_memory)},
        {"REQUEST_CPU": str(request_cpu)},
        {"REQUEST_MEM": str(request_memory)},
    ]

    train = dkube_training_op(
        auth_token=str(token),
        container='{"image":"polinux/stress"}',
        framework="custom",
        version="",
        program=str(code),
        run_script=str(run_script),
        envs=json.dumps(a),
    )
