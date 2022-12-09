FROM python:3
EXPOSE 8501

RUN pip install streamlit watchdog

COPY . /

CMD ["streamlit", "run", "webapp.py"]
