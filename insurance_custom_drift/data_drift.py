import numpy as np
import os, json
import pandas as pd
from scipy.stats import ks_2samp
from dkube.sdk import *
from dkube.sdk.utils.monitoring import get_configuration, baseline_from_schema

METRIC_FILE = "/tmp/metric.json"

class CustomDrift:
    def __init__(self):
        self.features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']

    def load_trainData_ref(self):
        train_data_file = os.path.join(os.getenv('MM_HOME'), "dc/train.npy")
        self.train_data = np.load(train_data_file)

    def get_predict_data(self):
        train_df = pd.DataFrame(data=self.train_data,
                                        columns=self.features)
        no_of_samples = np.random.randint(10,20)
        predict_df = pd.DataFrame()
        for each_col in self.features:
            predict_df[each_col] = train_df[each_col].sample(no_of_samples).values
        return predict_df

    def calculate_drift(self, x, metric="p_val"):
        result = {"data":{}, "meta":{}}
        for i in range(len(self.features)):
            feature = self.features[i]
            result["data"][feature] = {}
            ks = ks_2samp(self.train_data[:,i], x[:,i])
            if metric == "p_val":
                result["data"][feature]["drift"] = 1 - ks[1]
            else:
                result["data"][feature]["drift"] = 1 - ks[0]
        result["meta"]["num_samples"] = x.shape[0]
        return result

    def save_drift_scores(self, scores, predict_baseline):
        drift_metrics = {"scores":scores, "baseline":predict_baseline}
        with open(METRIC_FILE, 'w') as fp:
            json.dump(drift_metrics, fp, indent=4)

if __name__ == "__main__":
    mm_config = get_configuration()
    api = DkubeApi(token=os.getenv("DKUBE_USER_ACCESS_TOKEN"))
    mm_id = mm_config["envs"]["MM_UUID"]
    schema_df = api.modelmonitor_schema_to_df(mm_id)
    custom_drift = CustomDrift()
    custom_drift.load_trainData_ref()
    predict_df = custom_drift.get_predict_data()
    scores = custom_drift.calculate_drift(predict_df.values)
    predict_data_baseline = baseline_from_schema(predict_df, schema_df)
    custom_drift.save_drift_scores(scores, predict_data_baseline)
