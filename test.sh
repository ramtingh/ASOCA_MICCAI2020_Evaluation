#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

docker volume create asoca-output

docker run --rm \
        --memory=4g \
        -v $SCRIPTPATH/test/:/input/ \
        -v asoca-output:/output/ \
        asoca

docker run --rm \
        -v asoca-output:/output/ \
        python:3.7-slim cat /output/metrics.json | python -m json.tool

docker volume rm asoca-output
