library(reticulate)
dkube <- import("dkube")

token <- Sys.getenv("DKUBE_USER_ACCESS_TOKEN")
user <- Sys.getenv("LOGNAME")

coderepo <- 'https://github.com/oneconvergence/dkube-examples/tree/master/tf/classification/mnist/digits/classifier/program'
datarepo <- 'https://github.com/oneconvergence/dkube-examples/tree/master/tf/classification/mnist/digits/classifier/data'

generate <- dkube$sdk$rsrcs$util$generate

dkubeapi <- dkube$sdk$DkubeApi
api <- dkubeapi(token = token)

code_name <- generate("mnist")
code <- dkube$sdk$rsrcs$DkubeCode(user, name = code_name)
code$update_git_details(coderepo)
api$create_code(code)

dataset_name <- generate("mnist")
dataset <- dkube$sdk$rsrcs$DkubeDataset(user, name = dataset_name)
dataset$update_dataset_source(source='git')
dataset$update_git_details(datarepo)
api$create_dataset(dataset)

model_name <- generate("mnist")
model <- dkube$sdk$rsrcs$DkubeModel(user, name = model_name)
model$update_model_source(source='dvs')
api$create_model(model)
