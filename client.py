import sys

sys.path.insert(0, '/home/dkube/ahmed/dkube-sdk/dkube')

from dkube.sdk.dkube import *
import os

if __name__ == "__main__":
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkIjoxNTc5NjExMzQzLCJyb2xlIjoib3BlcmF0b3IiLCJ1c2VybmFtZSI6Im9jIn0.KyvXEmRdnSIZxzu-0s2z_atDUpKRxyradp_bFYNdyng'
    env = Environment(scheme='https', host='35.247.21.0', user='oc', token=token, port=32222)

    clinical_train  = {'name': 'clinical-train', 'mountpath': '/opt/dkube/inputs/train/clinical'}
    clinical_test   = {'name': 'clinical-test',  'mountpath': '/opt/dkube/inputs/test/clinical' }
    clinical_val    = {'name': 'clinical-val',    'mountpath': '/opt/dkube/inputs/val/clinical'  }

    images_train    = {'name': 'images-train',  'mountpath': '/opt/dkube/inputs/train/images' }
    images_test     = {'name': 'images-test',   'mountpath': '/opt/dkube/inputs/test/images'  }
    images_val      = {'name': 'images-val',    'mountpath': '/opt/dkube/inputs/val/images'   }

    rna_train       = {'name': 'rna-train',     'mountpath': '/opt/dkube/inputs/train/rna'  }
    rna_test        = {'name': 'rna-test',      'mountpath': '/opt/dkube/inputs/test/rna'   }
    rna_val         = {'name': 'rna-val',       'mountpath': '/opt/dkube/inputs/val/rna'    }
    
    launch_training_job("test", autogenerate=True, environ=env.external, 
            workspace='regression', script='python train_nn.py --epochs 5',
            datasets=[clinical_train, clinical_test, clinical_val, images_train, images_test, images_val, rna_train, rna_test, rna_val], 
            models=['dkube-regression-model'], template='regression-training')
    
    
    #export_model("/tmp/test-model", "test", autogenerate=True, environ=env.external, framework=Framework.Unknown)
