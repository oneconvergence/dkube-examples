FROM python:3
EXPOSE 8501
EXPOSE 8502
EXPOSE 8503

RUN pip install streamlit


COPY . /

CMD ["streamlit", "run", "webapp.py"]
