#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from dkube.sdk import *

import warnings
warnings.filterwarnings("ignore")
import requests, argparse
requests.packages.urllib3.disable_warnings()

# Set up the variables for Dataset Access

DATASET_INPUT_DIR = "/input/dataset/"
DATASET_OUTPUT_DIR = "/output/dataset/"

# Preprocess Data

## Get the original data from the input dataset repo mount point & write to output dataset
data = pd.read_csv(DATASET_INPUT_DIR + 'insurance.csv')

## Remove the AGE column & write out the new output to a new version of dataset
insurance_filtered = data.drop('age', axis=1)
insurance_filtered.to_csv(DATASET_OUTPUT_DIR + 'insurance.csv')
