#!/usr/bin/env bash

./build.sh

docker save asoca | gzip -c > ASOCA.tar.gz
