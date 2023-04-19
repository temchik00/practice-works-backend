#!/bin/bash

if [ "$DEBUG" = "true" ]; then
  echo 'debug mode'
  ./migrate.sh && uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
else
  echo 'production mode'
  ./migrate.sh && uvicorn app.main:app --host 0.0.0.0 --port 8002
fi
