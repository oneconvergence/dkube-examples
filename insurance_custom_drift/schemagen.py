from dkube.sdk.utils.monitoring import get_configuration, \
    infer_tabular_schema, baseline_from_schema
import pandas as pd
from dkube.sdk import *
import os
from sklearn import preprocessing
import json

def load_traindata(mm_config):
    train_data_location = mm_config.get("datasources", {}).get("train", {}).get("location")
    # loading train data
    if train_data_location:
        df = pd.read_csv(train_data_location)
    else:
        df = pd.read_csv("https://dkube-examples-data.s3.us-west-2.amazonaws.com/monitoring-insurance/training-data/insurance.csv")
    return df

def preprocess_data(df):
    for col in ['sex', 'smoker', 'region']:
        if (df[col].dtype == 'object'):
            le = preprocessing.LabelEncoder()
            le = le.fit(df[col])
            df[col] = le.transform(df[col])
            print('Completed Label encoding on',col)
    return df


if __name__ == "__main__":
    # getting model monitor configuration
    mm_config = get_configuration()

    # loading and preprocessing train data
    data_df = load_traindata(mm_config)

    data_df = preprocess_data(data_df)

    # infering schema from train data
    schema = infer_tabular_schema(data_df)

    # modifying schema
    schema["selected"] = True
    schema.loc[schema.label == "charges", "type"] = "prediction_output"

    # Initializing the dkube_api handler and posting the schema
    api = DkubeApi(token=os.getenv("DKUBE_USER_ACCESS_TOKEN"))

    cluster_id = mm_config["envs"].get("CLUSTER_ID", "")

    api.modelmonitor_update_schema_from_df(mm_config["envs"]["MM_UUID"],
                                            schema, cluster_id)

    # generating and publishing baseline
    baseline = baseline_from_schema(data_df, schema)

    api.publish_baseline(baseline, mm_config)

    # saving preprocessed train data for fit
    filepath = os.path.join(os.getenv('MM_HOME'), "processed.csv")
    data_df = data_df[['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']]
    data_df.to_csv(filepath, index=False)

    ## saving the train data baseline
    train_dist_file = "train_baseline.json"
    with open(train_dist_file, 'w') as fp:
        json.dump(baseline, fp, indent=4)
