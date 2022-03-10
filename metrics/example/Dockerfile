FROM python:3

ADD metrics.py /

ENV MONITOR_ID ""

RUN pip install requests

CMD [ "python", "./metrics.py" ]
