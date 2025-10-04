#!/bin/bash

CDIR="$(cd $(dirname $0) && pwd)"
docker build --rm -f "$CDIR/Dockerfile" -t sphinx:7.4.7-dev "$CDIR"
