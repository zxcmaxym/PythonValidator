#!/bin/bash

if [ -z "$1" ]; then
	echo "Task parameter not supplied"
	exit 1
fi

TASK_NAME=$1
echo $TASK_NAME

docker build --build-arg TASK=$TASK_NAME -t $TASK_NAME ./Docker/

docker create --name $TASK_NAME $TASK_NAME

docker start $TASK_NAME

sleep 1

docker cp ./Tasks/$TASK_NAME/* $TASK_NAME:/App/StudentWork/
