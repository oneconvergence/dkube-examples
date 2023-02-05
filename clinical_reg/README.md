## Create Project(optional)
1. Go to project tab and create a project with name "clinical-reg"

## Download pipeline to Jupyterlab
1. Start any of the jupyterlab notebook from the IDE tab.
   1. If project was created then create the IDE under the same Project.
   
   **Note:** If project is not created then it will got created during the below ipynb run.
2. Once running, click the jupyterlab icon to launch jupyterlab
3. Open terminal in Jupyterlab and run
   ```
   > wget https://raw.githubusercontent.com/oneconvergence/dkube-examples/tensorflow/clinical_reg/pipeline_withslurm.ipynb
   ```
4. Open pipeline.ipynb and run cells to generate the tar file and create run.
5. Download the tar file by right-clicking on it(optional).
6. Upload the tar file into the DKube pipeline UI(optional).

# Deploy model.(Optional)
-  Go to Model Catalog and from model version click deploy model.
-  Give name. 
-  Serving image: default 
-  Deployment type: Test
-  Select transformer
   -  Transformer script: `clinical_reg/transformer.py`
-  Deploy using: CPU and Submit. 
-  Deployed Model will be available in Model Serving.

## Test Inference.

1. Download the csv data file [cli_inp.csv](sample_data/cli_inp.csv) and any sample image from images folder from [sample_data/images](sample_data/images)
2. open https://{your-dkube-url}/inference,
   - Eg: https://1.2.3.4:32222/#/dsinference
3. In DKube UI, once the pipeline run has completed, navigate to ‘Deployments’ on the left pane
4. Copy the ‘Endpoint’ URL in the row using the clipboard icon
5. Enter the Endpoint URL into the Model Serving URL field of inference page,
6. Copy the token from ‘Developer Settings’ and paste into ‘Authorization Token’ box
7. Select Model Type as ‘Regression’ on the next dropdown selection
8. Click ‘Upload Image’ to load image from [1], ‘Upload File’ to load csv from [1]
9.  Click ‘Predict’ to run Inference.

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
4. Open workflow.ipynb from location `workspace/regression/clinical_reg` 
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
   - Framework version : 2.0.0
   - Startup command: python workflow.py 
   - Datasets: 
        - i.   clinical Mount point: /opt/dkube/input/clinical 
        - ii.  images Mount point: /opt/dkube/input/images 
        - iii. rna Mount Point: /opt/dkube/input/rna 
   - Output model: workflow, Mount point : /opt/dkube/output
