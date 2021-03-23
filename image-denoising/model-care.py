import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import numpy as np
import sys
import torch
import os
sys.path.append('../')
from unet.model import UNet
from pn2v import utils
from pn2v import histNoiseModel
from pn2v import training
from tifffile import imread
from pn2v.utils import denormalize
from pn2v.utils import normalize
from pn2v.utils import PSNR
from pn2v import prediction
import mlflow
import shutil
import requests
import argparse

CLASS_FILE = 'Net.py'

if not os.path.exists('/opt/dkube/output'):
    os.makedirs('/opt/dkube/output')
MODEL_DIR='/opt/dkube/output'
DATA_DIR='/opt/dkube/input'

STEPS=int(os.getenv('STEPS',5))
BATCH_SIZE = int(os.getenv('BATCHSIZE', 1))
EPOCHS = int(os.getenv('EPOCHS', 10))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
nameModel='convallaria_care'

def get_data(data_flag):
    fileName=DATA_DIR+'/20190520_tl_25um_50msec_05pc_488_130EM_Conv.tif'
    data=imread(fileName)
    if(data_flag=='train_data'):
        dataGT = np.mean(data, axis=0)[np.newaxis,...,np.newaxis]
        data=data[...,np.newaxis]
        dataGT = np.repeat(dataGT, 100, axis=0)
        data = np.concatenate((data,dataGT),axis=-1)
        my_train_data=data[:-5].copy()
        my_val_data=data[-5:].copy()
        return my_train_data,my_val_data
    if(data_flag=='test_data'):
        dataTest=imread(fileName)[:,:512,:512] 
        dataTestGT=np.mean(dataTest[:,...],axis=0)[np.newaxis,...]
        return dataTest,dataTestGT

def metric_evaluation(dataTest,dataTestGT):
    careRes=[]
    resultImgs=[]
    inputImgs=[]
    model = UNet(1,depth=3)
    model.load_state_dict(torch.load(MODEL_DIR+'/model.pt'))
    model.eval()
    ## Testing on 5 images for demo purpose
    for index in range(5):
        im=dataTest[index]
        gt=dataTestGT[0] # The ground truth is the same for all images
        careResult = prediction.tiledPredict(im, model ,ps=256, overlap=48,device=device, noiseModel=None)
        inputImgs.append(im)
        rangePSNR=np.max(gt)-np.min(gt)
        carePrior=PSNR(gt, careResult, rangePSNR )
        careRes.append(carePrior) 
    print("Avg PSNR CARE:", np.mean(np.array(careRes) ), '+-(2SEM)',2*np.std(np.array(careRes) )/np.sqrt(float(len(careRes)) ) )
    #### Logging the metric using mlflow #######
    mlflow.log_metric("Avg_PSNR_CARE",np.mean(np.array(careRes)))

def log_metrics(key, value, epoch, step):
    url = "http://dkube-exporter.dkube:9401/mlflow-exporter"
    train_metrics = {}
    train_metrics['mode']="train"
    train_metrics['key'] = key
    train_metrics['value'] = value
    train_metrics['epoch'] = epoch
    train_metrics['step'] = step
    train_metrics['jobid']=os.getenv('DKUBE_JOB_ID')
    train_metrics['run_id']=os.getenv('DKUBE_JOB_UUID')
    train_metrics['username']=os.getenv('DKUBE_USER_LOGIN_NAME')
    requests.post(url, json = train_metrics)

def main():
    try:
      fp = open(os.getenv('DKUBE_JOB_HP_TUNING_INFO_FILE', 'None'),'r')
      hyperparams = json.loads(fp.read())
      hyperparams['num_epochs'] = EPOCHS 
    except:
      hyperparams = {"batch_size": BATCH_SIZE, "num_epochs": EPOCHS, "learning_rate": 1e-3 }
      pass
    parser = argparse.ArgumentParser(description='Image Denoising Example')
    parser.add_argument('--learning_rate', type=float, default=float(hyperparams['learning_rate']), help='Learning rate for training.')
    parser.add_argument('--batch_size', type=int, default=int(hyperparams['batch_size']),
                        help='input batch size for training (default: 1024)')
    parser.add_argument('--num_epochs', type=int, default=int(hyperparams['num_epochs']),
                        help='number of epochs to train (default: 10)')
    global FLAGS
    FLAGS, unparsed = parser.parse_known_args()
    my_train_data,my_val_data=get_data('train_data')
    #### Start Training ####
    net = UNet(1, depth=3)
    trainHist, valHist = training.trainNetwork(net=net,trainData=my_train_data, valData=my_val_data,postfix=nameModel, directory=MODEL_DIR, noiseModel=None,numOfEpochs=FLAGS.num_epochs, stepsPerEpoch=STEPS,device=device, virtualBatchSize=20, batchSize=FLAGS.batch_size, learningRate=FLAGS.learning_rate, supervised=True)
    ### Copying the Class File to Model Directory ###
    shutil.copyfile(CLASS_FILE , os.path.join(MODEL_DIR,CLASS_FILE.split('/')[-1]))
    #### Metric Evaluation ####
    dataTest,dataTestGT = get_data('test_data')
    metric_evaluation(dataTest,dataTestGT)
    #### Logging the metrics #####
    step=1
    for i in range(0,FLAGS.num_epochs):
        log_metrics('Validation_Loss', valHist[i], i+1, step)
        step=step+1
    
    for i in range(0,FLAGS.num_epochs):
        log_metrics('Training_Loss', trainHist[i], i+1, step)
        step=step+1

if __name__ == '__main__':
    main()
