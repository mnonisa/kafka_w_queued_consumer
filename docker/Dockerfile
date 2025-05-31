FROM python:3.10-slim

RUN apt-get update -y
RUN apt-get install vim -y
RUN apt-get install procps -y
RUN apt-get install git -y

ENV PROJECT_BASE=/usr/local/app
WORKDIR $PROJECT_BASE

COPY app/resources/requirements.txt $PROJECT_BASE

RUN mkdir /usr/local/app/tmp
RUN mkdir /usr/local/app/downloads

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "producer.py"]