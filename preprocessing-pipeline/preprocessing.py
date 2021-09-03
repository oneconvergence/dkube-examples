import os
import tensorflow as tf
import urllib.request
import shutil
import gzip


def download(DATA_DIR):
    filename="train-images-idx3-ubyte"
    filepath = os.path.join(DATA_DIR, filename)
    if not tf.io.gfile.exists(DATA_DIR):
        tf.io.gfile.makedirs(DATA_DIR)
    url = "https://storage.googleapis.com/cvdf-datasets/mnist/"+filename+".gz"
    zipped_filepath = filepath + '.gz'
    urllib.request.urlretrieve(url, zipped_filepath)
    with gzip.open(zipped_filepath, 'rb') as f_in, open(filepath, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(zipped_filepath)

if __name__ == "__main__":
    
    DATA_DIR = '/opt/dkube/input'
    download(DATA_DIR)
