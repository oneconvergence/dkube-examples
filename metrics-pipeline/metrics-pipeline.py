import json
import os

import kfp

search_path = os.path.dirname(os.path.abspath(__file__)) + "/../components"
component_store = kfp.components.ComponentStore(local_search_paths=[search_path])

dkube_job_op = component_store.load_component("job")


@kfp.dsl.pipeline(name="Metrics pipeline")
def metrics_pipeline(code, predict_script, token):
    _ = dkube_job_op(
        "metrics",
        str(token),
        json.dumps({"image": "ocdr/dkube_pylauncher:2.3"}),
        program=str(code),
        run_script=str(predict_script),
        file_outputs={"mlpipeline-ui-metadata": "/output/metrics.json"},
    )

