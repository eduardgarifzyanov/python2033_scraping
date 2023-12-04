FROM python:latest


USER root
RUN apt-get update
RUN pip install --upgrade pip

RUN mkdir parser
COPY /parser_project/. /parser

WORKDIR /parser

RUN pip install --no-cache-dir -r /parser/requirements.txt

RUN python connect_db.py

