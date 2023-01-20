FROM python:3
EXPOSE 8501

RUN pip install streamlit kafka-python

ARG CACHE_DATE=invalidate_cache
COPY *.py /

CMD ["streamlit", "run", "app.py", "--server.fileWatcherType=none"]
