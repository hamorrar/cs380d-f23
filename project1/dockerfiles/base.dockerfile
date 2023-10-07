FROM ubuntu:20.04

# MAINTAINER Hilal Morrar <hilal@utexas.edu> version: 0.1

USER root

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PYTHONUNBUFFERED=1

RUN apt-get update 
# && apt-get install -y git

# RUN git clone https://github.com/hamorrar/cs380d-f23.git

# COPY . /cs380d-f23/project1/server.py
# COPY . /cs380d-f23/project1/frontend.py

ENV KVS_HOME /cs380d-f23/project1
COPY scripts/dependencies2.sh ${KVS_HOME}/scripts/
COPY kubespray/requirements.txt ${KVS_HOME}/kubespray/

# Install dependencies
WORKDIR ${KVS_HOME}/scripts
RUN bash dependencies2.sh

WORKDIR /
