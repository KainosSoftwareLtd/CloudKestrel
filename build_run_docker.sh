#!/usr/bin/env bash

# Get current working directory
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Build Docker Image
docker build -t cloudkestrel .

# Run CloudKestrel in Docker
docker run --env-file environment_variables_docker.env -v $CWD:/host_dir cloudkestrel

# Return the result.  0 = No fails, Non Zero = X fails
echo $?