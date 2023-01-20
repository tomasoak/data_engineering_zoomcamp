FROM python:3.8-slim-buster

RUN apt-get install wget
RUN pip install pandas sqlalchemy

WORKDIR /week_01
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]