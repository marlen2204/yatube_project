FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /yatube_project

ADD ./yatube_project

RUN pip install -r requirements.txt
