import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import os, shutil
from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np


def read_file(filename):
    data = pd.read_csv(filename,encoding = "ISO-8859-1")
    return data


def split_csv(data, s_ratio, case, seed_val=42):
    chunks = []
    np.random.seed(seed_val)
    seeds = np.random.randint(1,45,3)
    i = 0
    if case == 1:
        for cr in s_ratio[:-1]:
            data, d = train_test_split(data, test_size=cr, random_state = seeds[i])
            chunks.append(d)
            i += 1
        chunks.append(data)
        return chunks, seeds
    elif case == 2:
        for cr in s_ratio:
            data, d = train_test_split(data, test_size=cr, random_state = seeds[i])
            chunks.append(d)
            i += 1
        return chunks, seeds
    elif case == 3:
        for cr in s_ratio:
            _ , d = train_test_split(data, test_size=cr, random_state = seeds[i])
            chunks.append(d)
            i += 1
        return chunks, seeds


def normalize_ratio(ratio, n_samples):
    if len(ratio) != 3:
        print("error: Ratio has less/more than three numbers")
        exit(1)
    if sum(ratio) <= 100:
        #ratio.reverse()
        c_sizes = [(r/100)*n_samples for r in ratio]
        norm = []
        items_left = n_samples
        for cs in c_sizes:
            cr = cs / items_left
            norm.append(cr)
            items_left -= cs
        if sum(ratio) == 100:
            case = 1
        else:
            case = 2
        return norm, case
    elif sum(ratio) > 100:
        case = 3
        norm = [r/100 for r in ratio]
        return norm, case
    else:
        print("Ratio is not correct")
        exit(1)

def split_imgs(seed, files, case):
    chunks = []
    np.random.seed(seed)
    seeds = np.random.randint(1,45,3)
    i = 0
    if case == 1:
        for cr in s_ratio[:-1]:
            files, d = train_test_split(files, test_size=cr, random_state = seeds[i])
            chunks.append(d)
            i += 1
        chunks.append(files)
        return chunks
    elif case == 2:
        for cr in s_ratio:
            files, d = train_test_split(files, test_size=cr, random_state = seeds[i])
            chunks.append(d)
            i += 1
        return chunks
    elif case == 3:
        for cr in s_ratio:
            _ , d = train_test_split(files, test_size=cr, random_state = seeds[i])
            chunks.append(d)
            i += 1
        return chunks

def save_csv_chunks(chunks, filename, outputdir, filetype):
    fname = os.path.splitext(filename)[0]
    fname = fname.split('/')[-1]
    ext = os.path.splitext(filename)[1]
    if not os.path.exists(outputdir[0]):
        os.makedirs(outputdir[0])
    chunks[0].to_csv(outputdir[0] + '/' + fname + '_' + 'train' + ext, index = 0)
    if not os.path.exists(outputdir[1]):
        os.makedirs(outputdir[1])
    chunks[1].to_csv(outputdir[1] + '/'  + fname + '_' + 'val' + ext, index = 0)
    if not os.path.exists(outputdir[2]):
        os.makedirs(outputdir[2])
    chunks[2].to_csv(outputdir[2] + '/'  + fname + '_' + 'test' + ext, index = 0)

def save_imgs(img_chunks, imgfolder, outputdir, filetype):
    if not os.path.exists(outputdir[0]):
        os.makedirs(outputdir[0])
    for f in img_chunks[0]:
        shutil.copy(imgfolder + f, outputdir[0])
        
    if not os.path.exists(outputdir[1]):
        os.makedirs(outputdir[1])
    for f in img_chunks[1]:
        shutil.copy(imgfolder + f , outputdir[1])
        
    if not os.path.exists(outputdir[2]):
        os.makedirs(outputdir[2])
    for f in img_chunks[2]:
        shutil.copy(imgfolder + f, outputdir[2])

if __name__== "__main__":
    parser = ArgumentParser(description="Split dataset into multiple chunks provided the ratio.\n"
                                        "Example: [python3 split.py --datatype [image, clinical, rna]"
                                        " --ratio 10 10 80 --seed 13 --outputdir data_splits/]", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-dtype","--datatype", dest = 'datatype',
                        required = True, help="input data type")
    parser.add_argument("-r","--ratio", dest="ratio", default=[75,15,10],nargs='+',
                        help="dataset split ratio", type=int)
    parser.add_argument("-s", "--seed",dest="seed", type=int,default=13,
                        help="a seed value for random generator,"
                             " helps in regenerating the split",)
    parser.add_argument("-o","--outputdir", default='/opt/dkube/outputs/', dest = 'outdir', help="output folder path")
    args = parser.parse_args()

    DATA_DIR = "/opt/dkube/input"
    OUT_DIR = args.outdir
    TRAIN_DATA = OUT_DIR + 'train/'
    VAL_DATA = OUT_DIR + 'val/'
    TEST_DATA = OUT_DIR + 'test/'
    filetype = args.datatype
    if filetype in ['clinical', 'rna']:
        if filetype == 'clinical':
            filename = DATA_DIR + '/cli_data_processed.csv'
        else:
            filename = DATA_DIR + '/mRNAseq.csv'
        raw_data = read_file(filename)
        data = read_file(filename)
        n_samples = len(data)
        s_ratio, case = normalize_ratio(args.ratio, n_samples)
        chunks, seeds = split_csv(data,s_ratio, case, args.seed)
        print(n_samples)
        save_csv_chunks(chunks, filename, [TRAIN_DATA, VAL_DATA, TEST_DATA], filetype)   
    elif filetype == 'image':
        imgfolder = DATA_DIR + '/'
        img_names = os.listdir(imgfolder)
        n_samples = len(img_names)
        s_ratio, case = normalize_ratio(args.ratio, n_samples)
        chunks = split_imgs(args.seed, img_names, case)
        save_imgs(chunks, imgfolder, [TRAIN_DATA, VAL_DATA, TEST_DATA], filetype)
    else:
        print('Unknown filetype passed, known filetypes are IMG, CLI, RNA')