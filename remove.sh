#!/bin/bash

NAME=$1
docker stop $NAME
docker rm $NAME
docker image rm $NAME
