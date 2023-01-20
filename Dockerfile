# Build an image that can serve models.
FROM ocdr/sklearnserver:0.23.2
RUN pip install kafka-python

ARG CACHE_DATE=invalidate_cache
COPY predictor-kafkaresp.py /mnt/predictor.py
ARG MODEL_PATH
COPY $MODEL_PATH /opt/ml/model

ENTRYPOINT ["python", "/mnt/predictor.py", "--model_dir=/opt/ml/model"]

#FROM ocdr/sklearnserver:0.23.2

#ARG MODEL_PATH
#COPY $MODEL_PATH /opt/ml/model

#ENTRYPOINT ["python", "-m", "sklearnserver", "--model_dir=/opt/ml/model"]
