#!/bin/bash

# In the future, this should rely on docker-compose

DOCKER_IMAGE=wbm-exclusion-tool

set -o allexport
source .env
set +o allexport

docker image build -t $DOCKER_IMAGE .
docker container run --rm -it -p 2000:8501 -e API_KEY=$API_KEY $DOCKER_IMAGE
