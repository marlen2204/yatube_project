FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /yatube_project/

ADD . .

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

