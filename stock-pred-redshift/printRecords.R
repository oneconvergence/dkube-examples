library(jsonlite)
library(httr)

ds <- fromJSON("/etc/dkube/redshift.json")

user <- Sys.getenv("LOGNAME")

url <- "http://dkube-controller-worker.dkube:5000/dkube/v2/controller/users/%s/datums/class/dataset/datum/%s"

token <- Sys.getenv("DKUBE_USER_ACCESS_TOKEN")

header_data <- sprintf("Bearer %s", token)

rs_fetch_datasets <- function(){
  for (row in 1:nrow(ds)){
    r <- GET(sprintf(url, Sys.getenv("LOGNAME"), ds[row, "rs_name"]), add_headers(Authorization = header_data))
    password <- content(r)$data$datum$redshift$password
    ds[row, "password"] <- password
  }
  ds
}

get_password <- function(user, db){
  datasets <- rs_fetch_datasets()
  for (row in 1:nrow(datasets)){
    if (datasets[row, "rs_user"] == user && datasets[row, "rs_database"] == db){
      return(datasets[row, "password"])
    }
  }
}

get_password("dpaks", "dkube")
