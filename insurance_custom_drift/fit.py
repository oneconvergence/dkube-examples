import numpy as np
import pandas as pd
import os

## In fit user can use custom method to save train data representation 
## which can be used during drift detection.

if __name__ == "__main__":
    mm_home = os.getenv('MM_HOME')
    filepath = os.path.join(mm_home, "processed.csv")
    train_data = pd.read_csv(filepath)

    dc_dir = os.path.join(mm_home, "dc")

    os.makedirs(dc_dir, exist_ok=True)

    # saving train data array for drift detection
    np.save(os.path.join(dc_dir, 'train.npy'), 
                train_data.values)
