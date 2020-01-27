FROM ubuntu:16.04
MAINTAINER kainos

# Install Python and other OS stuff
RUN apt-get update && \
    apt-get install -y build-essential \
      python3.5 \
      python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Required Python libraries
RUN pip3 install --upgrade pip
RUN pip3 install boto3

COPY . /usr/local/bin/cloudkestrel
RUN chmod +x /usr/local/bin/cloudkestrel/cloudkestrel.py
ENTRYPOINT [ "/usr/local/bin/cloudkestrel/cloudkestrel.py" ]