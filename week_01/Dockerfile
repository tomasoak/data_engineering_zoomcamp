FROM python:3.9

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get install wget
RUN python3 -m pip install --upgrade pip

WORKDIR /week_01
COPY ingest_data.py ingest_data.py
COPY requirements.txt . 

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python", "ingest_data.py" ]