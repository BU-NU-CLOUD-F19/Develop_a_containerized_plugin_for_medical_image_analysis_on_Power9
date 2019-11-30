#
# Dockerfile for pfioh repository.
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pfioh .
#
# In the case of a proxy (located at say 10.41.13.4:3128), do:
#
#    export PROXY="http://10.41.13.4:3128"
#    docker build --build-arg http_proxy=${PROXY} --build-arg UID=$UID -t local/pfioh .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --rm --entrypoint /bin/bash local/pfioh
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti --rm -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pfioh
#

FROM ubuntu:latest
MAINTAINER fnndsc "dev@babymri.org"

# Pass a UID on build command line (see above) to set internal UID
ARG UID=1001
ENV UID=$UID

COPY . /tmp/pfioh
COPY ./docker-entrypoint.py /dock/docker-entrypoint.py

RUN apt-get update \
  && apt-get install sudo                                             \
  && apt-get install -y python3.7                                     \ 
  && apt-get install -y python-pip                                    \
  && apt-get install --upgrade -y python3-pip                         \
  && useradd -u $UID -ms /bin/bash localuser                          \
  && addgroup localuser sudo                                          \
  && echo "localuser:localuser" | chpasswd                            \
  && adduser localuser sudo                                           \
  && apt-get install -y libssl-dev libcurl4-openssl-dev bsdmainutils vim net-tools inetutils-ping \
  && apt-get install -y libgnutls28-dev                               \
  && pip install --upgrade pip                                        \
  && pip3 install /tmp/pfioh                                          \  
  && rm -rf /tmp/pfioh                                                \
  && chmod 777 /dock                                                  \
  && chmod 777 /dock/docker-entrypoint.py                             \
  && echo "localuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENTRYPOINT ["/dock/docker-entrypoint.py"]
EXPOSE 5055

# Start as user $UID
# USER $UID
