#!/usr/bin/env bash

flask run --host 0.0.0.0 --port 5000 &
python $1/bash_entrypoint.py