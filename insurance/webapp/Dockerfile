FROM python:3
EXPOSE 8501

RUN pip install streamlit

COPY . /

CMD ["streamlit", "run", "webapp.py"]
