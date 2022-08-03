from prediction import TreeModel
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#max_depths = [5, 8, 10]
max_depths = [5]

if __name__ == '__main__':
    for n in max_depths:
        params = {"max_depth": n, "random_state": 42}
        dtc = TreeModel.create_instance(**params)
        exp_id, run_id = dtc.mlflow_run()
        print(f"MLflow Run completed with run_id {run_id} and experiment_id {exp_id}")
        print("<->" * 40)
