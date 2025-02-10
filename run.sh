#!/bin/bash
docker build -t test .
docker run -d --name test -v "/var/run/docker.sock":"/var/run/docker.sock" -p 4444:4444 test
