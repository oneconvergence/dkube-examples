## Compile file manually

a. Start any of the jupyterlab notebook from the IDE tab.
b. Once running, click the jupyterlab icon to launch jupyterlab
c. Open terminal in Jupyterlab and run
   ```
   > wget https://raw.githubusercontent.com/oneconvergence/dkubeio-examples/master/tf/clinical_reg/pipeline/pipeline.ipynb
   ```
d. Open pipeline.ipynb and run cells to generate the tar file and create run.
e. Download the tar file by right-clicking on it(optional).
f. Upload the tar file into the DKube pipeline UI(optional).


# Publish model.
1. Publish Model 
   -  From repo go to model and it's version, and click on the Published model.
   -  Give name. 
   -  Transformer script: `clinical_reg/transformer.py`
   -  Submit.


# Deploy model.
1. Deploy Model 
   -  Go to Model Catalog and from model version click deploy model.
   -  Give name. 
   -  Serving image: default 
   -  Deploy using: CPU and Submit. 
   -  Deployed Model will be available in Model Serving.

## Test Inference.

1. Download the data files cli_inp.csv and any sample image from images folder from https://github.com/oneconvergence/dkubeio-examples/tree/master/tf/clinical_reg/inference/data
2. In DKube UI, once the pipeline run has completed, navigate to ‘Test Inferences’ on the left pane
3. Copy the ‘Endpoint’ URL in the row using the clipboard icon
4. Duplicate DKube UI on a new tab and change the URL using the domain name and replacing the remaining path with inference after the domain name. 
   - For e.g, https://URL/inference or  https://1.2.3.4:32222/#/dsinference
5. Enter the following URL into the Model Serving URL box https://dkube-proxy.dkube
6. Copy the token from ‘Developer Settings’ and paste into ‘Authorization Token’ box
7. Select Model Type as ‘Regression’ on the next dropdown selection
8. Click ‘Upload Image’ to load image from [A], ‘Upload File’ to load csv from [A]
9. Click ‘Predict’ to run Inference.

## Regression Notebook Workflow(Repos will be created by the pipeline above).

1. Go to IDE section
2. Create Notebook 
   - Give a name 
   - Code: regression
   - Framework : Tensorflow
   - Framework version : 2.3
   - Datasets: 
         - i.   clinical Mount point: /opt/dkube/input/clinical 
         - ii.  images Mount point: /opt/dkube/input/images 
         - iii. rna Mount Point: /opt/dkube/input/rna
i3. Submit
4. Open workflow.ipynb from location `workspace/regression/tf/clinical_reg` 
   - Run cells and wait for output (In case of running the notebook second time, restart the kernel)
5. Delete if workflow.py is already there and export the workflow notebook as executable. 
   - Upload it into Juyterlab. 
   - Make changes in py file, comment/remove the following line numbers: 
        -i. 239-240
        -ii. 268 
        -iii. 435-end 
  -  Save and commit the workflow.py
6. Create a model named workflow with source none.
7. Create training run using workflow.py 
   - Give a name 
   - Code: regression 
   - Framework : Tensorflow
   - Framework version : 1.14
   - Startup command: python workflow.py 
   - Datasets: 
        - i.   clinical Mount point: /opt/dkube/input/clinical 
        - ii.  images Mount point: /opt/dkube/input/images 
        - iii. rna Mount Point: /opt/dkube/input/rna 
   - Output model: workflow, Mount point : /opt/dkube/output



