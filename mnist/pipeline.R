library("reticulate")
kfp <- import("kfp")
dkube <-import("dkube")

username <- Sys.getenv("USERNAME")
token <- Sys.getenv("DKUBE_USER_ACCESS_TOKEN")
client <- kfp$Client(existing_token=token)
api <- dkube$sdk$DkubeApi(token=token)

code_name <- "r-examples"
model_name <- "mnist"
dataset_name <- "mnist"
image = "ocdr/dkube-datascience-rs-tf-cpu:v2.0.0-1"


training <- dkube$sdk$rsrcs$DkubeTraining(username, name="train")
training$update_container(framework="tensorflow_r-2.0.0", image_url=image)
training$add_code(code_name, commitid="")
training$update_startupscript("python mnist/train.R")
training$add_input_dataset(dataset_name, mountpath='/mnist')
training$add_output_model(model_name, mountpath='/model')
training$add_envvar("EPOCHS","1")

serving = dkube$sdk$rsrcs$DkubeServing(username, name="serving")
serving$set_transformer(TRUE, script='mnist/transformer.py')
serving$update_serving_model(model_name)

mnist_pipeline <- function(token = "",  dummy = "Empty"){
  train <- dkube$pipelines$dkube_training_op("train", authtoken=token, training=training)
  serving <- dkube$pipelines$dkube_serving_op("serve", authtoken=token, serving=serving)$after(train)
}

arguments <- list(args = token, kwargs="")
client$create_run_from_pipeline_func(r_to_py(mnist_pipeline), arguments)

kfp$compiler$Compiler()$compile(mnist_pipeline, 'mnist_pl.tar.gz') 
