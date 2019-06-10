#!/bin/bash
export PYTHONPATH=$PWD/
python ./my_opcua_client/webs.py &
python ./my_opcua_client/k6_client.py

