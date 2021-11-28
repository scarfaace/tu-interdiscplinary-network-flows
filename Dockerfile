FROM ubuntu:20.04

COPY experiments ./
COPY labeling ./
COPY requirements.txt ./

ENV VENV_NAME="venv"

RUN apt update -y && apt upgrade -y
RUN apt install python3-pip -y
RUN pip3 install virtualenv

RUN virtualenv $VENV_NAME
RUN chmod 755 $VENV_NAME/bin/activate && \
    ./$VENV_NAME/bin/activate
RUN pip install -r requirements.txt