FROM ocdr/dkube-datascience-tf-cpu:v2.0.0-1

COPY . .

ENTRYPOINT ["python3", "regressionsetup.py"]
