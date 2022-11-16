from cloudpathlib import CloudPath

def download_to(s3path, localpath):
    cp = CloudPath(s3path)
    cp.download_to(localpath)

def upload_from(localpath, s3path):
    cp = CloudPath(s3path)
    cp.upload_from(localpath)

def delete(s3path):
    cp = CloudPath(s3path)
    cp.rmtree()

def syncfrom(localpath, s3path):
    delete(s3path)
    upload_from(localpath, s3path)
