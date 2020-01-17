#!/usr/bin/env bash

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build -t cloudkestrel .

docker run --env-file environment_variables_docker.env -v $CWD:/host_dir cloudkestrel
echo $?