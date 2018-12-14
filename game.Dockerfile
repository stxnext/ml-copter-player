FROM ubuntu:16.04

ARG USER_ID

ADD . /workspace
WORKDIR /workspace

RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3.6 -m pip install pip --upgrade && \
        python3.6 -m pip install wheel

RUN pip install -r requirements.txt

RUN adduser --shell /bin/bash --disabled-password --gecos "" --uid $USER_ID game
RUN chown -R game /workspace
USER game


CMD ["python3.6", "app.py"]
