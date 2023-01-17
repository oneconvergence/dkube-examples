import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import os
from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np

def continious_to_categorical(data):
    median = data.median()
    low = data.min()
    high = data.max()
    lmedian = (low+median)/2
    rmedian = (high+median)/2
    temp = []
    for v in data:
        if v < (lmedian+median)/2:
            temp.append(1)
        elif v > (rmedian+median)/2:
            temp.append(2)
        else:
            temp.append(3)
    return pd.Series(temp)

def read_file(filename):
    data = pd.read_csv(filename,encoding = "ISO-8859-1")
    return data

coi = ['vital_status', 'bcr_patient_barcode',
      'age_at_initial_pathologic_diagnosis','bcr_patient_canonical_status',
      'days_to_birth','ethnicity', 'gender',
      'histological_type', 'history_of_neoadjuvant_treatment',
      'initial_pathologic_diagnosis_method', 'karnofsky_performance_score',
      'performance_status_scale_timing', 'person_neoplasm_cancer_status',
      'postoperative_rx_tx', 'prior_glioma','tissue_source_site','days_to_death']

string_features = ['vital_status', 'ethnicity', 'bcr_patient_canonical_status',
                  'gender', 'histological_type', 'history_of_neoadjuvant_treatment',
                  'initial_pathologic_diagnosis_method', 'performance_status_scale_timing',
                  'person_neoplasm_cancer_status', 'postoperative_rx_tx', 'prior_glioma',
                  'tissue_source_site']
range_f = ['age_at_initial_pathologic_diagnosis']
ctn_r = ['age_at_initial_pathologic_diagnosis', 'days_to_birth', ]
ctn_min_max = ['karnofsky_performance_score']


if __name__== "__main__":
    parser = ArgumentParser(description="Preprocess clinical data.\n"
                                        "Example: [python3 pre-processing.py --filename csv/All_CDEs.csv "
                                        "--outputfile csv/cli_data_processed.csv]", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-f","--filename", dest = 'filename', required=False, help="input file path")
    parser.add_argument("-o","--outputfile", required=False, dest = 'outfile', help="output folder path")
    args = parser.parse_args()


    filename = "/opt/dkube/input/All_CDEs.csv"
    #filename = args.filename     #filename = "csv/All_CDEs.csv"
    #outfile = args.outfile # 'csv/cli_data_processed.csv'
    outfile = "/opt/dkube/output/cli_data_processed.csv"
    data = read_file(filename)
    data = data[coi]
    data = data.fillna(0)
    data[string_features] = data[string_features].apply(lambda x: pd.factorize(x)[0] + 1)
    float_array = data['karnofsky_performance_score'].values.astype(float)
    float_array = float_array.reshape(float_array.shape[0],1)
    min_max_scaler = preprocessing.MinMaxScaler()
    scaled_array = min_max_scaler.fit_transform(float_array)
    data['karnofsky_performance_score'] = pd.DataFrame(scaled_array)
    data['age_at_initial_pathologic_diagnosis'] = continious_to_categorical(data['age_at_initial_pathologic_diagnosis'])
    data['days_to_birth'] = continious_to_categorical(data['days_to_birth'])

    float_array = data['days_to_death'].values.astype(float)
    float_array = float_array.reshape(float_array.shape[0],1)
    min_max_scaler = preprocessing.MinMaxScaler()
    scaled_array = min_max_scaler.fit_transform(float_array)
    data['days_to_death'] = pd.DataFrame(scaled_array)

    data.to_csv(outfile, index = 0)
