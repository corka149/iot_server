FROM python:3.8-buster

# SETUP
RUN mkdir /iot_server
WORKDIR /iot_server
ADD . /iot_server
RUN pip3 install -r requirements.txt

# SECURITY
RUN groupadd -r iotserver && useradd -r -s /bin/false -g iotserver iotserver
RUN chown -R iotserver:iotserver /iot_server
USER iotserver

# RUN
ENV PYTHONPATH=src
CMD gunicorn -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker iot_server.main:api --name iot_server --chdir /iot_server --user iotserver
