import sys, time
from dkube.sdk import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--auth_token',dest = 'authtoken', type=str)
parser.add_argument('--user',dest = 'user', type=str)
args = parser.parse_args()

authToken = args.authtoken
user = args.user

print(user)

api = DkubeApi(token=authToken)
try:
    res = api.get_code(user, 'regression')
    print("Datum already exists")
except:
    code = DkubeCode(user, name='regression')
    code.update_git_details('https://github.com/oneconvergence/dkubeio-examples/tree/master/tf/clinical_reg')
    api.create_code(code)

try:
    res = api.get_dataset(user, 'clinical')
    print("Datum already exists")
except:
    dataset = DkubeDataset(user, name='clinical')
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkubeio-examples-data/tree/master/tf/clinical_reg/clinical')
    api.create_dataset(dataset)

try:
    res = api.get_dataset(user, 'images')
    print("Datum already exists")
except:
    dataset = DkubeDataset(user, name='images')
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkubeio-examples-data/tree/master/tf/clinical_reg/image_data')
    api.create_dataset(dataset)
    
try:
    res = api.get_dataset(user, 'rna')
    print("Datum already exists")
except:
    dataset = DkubeDataset(user, name='rna')
    dataset.update_dataset_source(source='git')
    dataset.update_git_details('https://github.com/oneconvergence/dkubeio-examples-data/tree/master/tf/clinical_reg/rna')
    api.create_dataset(dataset)

    
dvs_datasets = ['clinical-preprocessed', 'clinical-train', 'clinical-test', 'clinical-val',
                'images-preprocessed', 'images-train', 'images-test', 'images-val',
                'rna-train', 'rna-test', 'rna-val']

for each_dataset in dvs_datasets:
    try:
        res = api.get_dataset(user, name=each_dataset)
        print("Datum already exists")
    except:
        dataset = DkubeDataset(user, name=each_dataset)
        dataset.update_dataset_source(source='dvs')
        api.create_dataset(dataset)
 
try:
    res = api.get_model(user, 'regression-model')
    print("Datum already exists")
except:
    model = DkubeModel(user, name='regression-model')
    model.update_model_source(source='dvs')
    api.create_model(model)
print("Finishing Resources creation")
time.sleep(60)

