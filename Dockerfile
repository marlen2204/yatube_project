FROM python:3

ENV PYTHONUNBUFFERED 1

<<<<<<< HEAD
WORKDIR /yatube_project/

ADD . .

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt
=======
WORKDIR /yatube_project

ADD ./yatube_project

RUN pip install -r requirements.txt
>>>>>>> origin/main
