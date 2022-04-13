library(reticulate)
dkube <- import("dkube")

token <- Sys.getenv("DKUBE_USER_ACCESS_TOKEN")
user <- Sys.getenv("LOGNAME")

generate <- dkube$sdk$rsrcs$util$generate
dkubeapi <- dkube$sdk$DkubeApi
api <- dkubeapi(token = token)

code_name <- 'mnist-0067'
dataset_name <- 'mnist-1532'
model_name <- 'mnist'
training_code <- "python model.py"
transformer_code <- "tf/classification/mnist-fs/digits/transformer/transformer.py"
framework <- "tensorflow_1.14"
training_image <- "ocdr/d3-datascience-tf-cpu:fs-v1.14"
inp_path <- "/opt/dkube/input"
out_path <- "/opt/dkube/output"

training_name <- generate('mnist')
training <- dkube$sdk$rsrcs$DkubeTraining(user, name=training_name, description='triggered from dkube sdk')
training$update_container(framework=framework, image_url=training_image)
training$update_startupscript(training_code)
training$add_code(code_name)
training$add_input_dataset(dataset_name, mountpath=inp_path)
training$add_output_model(model_name, mountpath=out_path)
api$create_training_run(training)

serving_name <- generate('mnist')
serving <- dkube$sdk$rsrcs$DkubeServing(user, name=serving_name, description='serving deployed from dkube sdk')
serving$update_transformer_code(code=code_name, code=transformer_code)
serving$update_transformer_image(image_url=training_image)
serving$update_serving_model(model_name)
serving$update_serving_image(image_url='ocdr/tensorflowserver:1.14')
api$create_test_inference(serving)
