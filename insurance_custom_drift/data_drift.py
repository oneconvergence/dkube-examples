import numpy as np
import os, json
import pandas as pd
from scipy.stats import ks_2samp
from dkube.sdk import *
from dkube.sdk import CUSTOM_METRICS_FILE
from dkube.sdk.utils.monitoring import get_configuration, compute_distributions_from_schema

class CustomDrift:
    def __init__(self):
        self.features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']

    def load_trainData_ref(self):
        train_data_file = os.path.join(os.getenv('MM_HOME'), "dc/train.npy")
        self.train_data = np.load(train_data_file)

    def get_predict_data(self):
        '''
        Function to generate random predict data, 
        In user's case user code would pull data from 
        predict data source
        '''
        train_df = pd.DataFrame(data=self.train_data,
                                        columns=self.features)
        no_of_samples = np.random.randint(10,20)
        predict_df = pd.DataFrame()
        for each_col in self.features:
            predict_df[each_col] = train_df[each_col].sample(no_of_samples).values
        return predict_df

    def calculate_drift(self, x, metric="p_val"):
        '''
        Function to calculate the drift, 
        This function can be modified to
        calculate drift using custom algorithm.
        '''
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
        '''
        Function to dump drift scores
        '''
        drift_metrics = {"scores":scores, "distributions":predict_baseline}
        with open(CUSTOM_METRICS_FILE, 'w') as fp:
            json.dump(drift_metrics, fp, indent=4, default=str)

if __name__ == "__main__":
    # loafing model monitor configuration
    mm_config = get_configuration()
    # Initializing DKube API
    api = DkubeApi(token=os.getenv("DKUBE_USER_ACCESS_TOKEN"))
    mm_id = mm_config["envs"]["MM_UUID"]
    # Loading model monitor schema to dataframe.
    schema_df = api.modelmonitor_schema_to_df(mm_id)
    custom_drift = CustomDrift()
    custom_drift.load_trainData_ref()
    # loading predict data
    predict_df = custom_drift.get_predict_data()
    # calculating drift scores
    scores = custom_drift.calculate_drift(predict_df.values)
    # computing predict data distributions. schema is required to compute distributions.
    predict_data_distributions = compute_distributions_from_schema(predict_df, schema_df)
    # saving the scores and predict data distributions
    custom_drift.save_drift_scores(scores, predict_data_distributions)
    ## validating the saved scores
    print("scores and baseline saved in CUSTOM_METRICS_FILE i.e /tmp/metrics.json")
    with open(CUSTOM_METRICS_FILE) as f:
        data = json.load(f)
    print(data)
