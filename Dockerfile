# Build an image that can serve models.
FROM ocdr/sklearnserver:0.23.2

ARG MODEL_PATH
COPY $MODEL_PATH /opt/ml/model

ENTRYPOINT ["python", "-m", "sklearnserver", "--model_dir=/opt/ml/model"]
