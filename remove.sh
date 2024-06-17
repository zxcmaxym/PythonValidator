#!/bin/bash

NAME=$1
docker rm $NAME
docker image rm $NAME
