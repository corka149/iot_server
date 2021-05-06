#!/usr/bin/env sh

if [ -z $IOT_SERVER_PROFILE ]; then
  echo 'No profile set in $IOT_SERVER_PROFILE.'
  exit 1
fi

gunicorn -b 0.0.0.0:8000 -w 1 -k uvicorn.workers.UvicornWorker iot_server.main:app --name iot_server --chdir /iot_server --user iotserver
