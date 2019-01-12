#!/usr/bin/env bash

. venv/bin/activate
export FLASK_APP=drinklist-api
export FLASK_DEBUG=1  # to enable autoreload
export FLASK_ENV=debug

# start server
flask run
