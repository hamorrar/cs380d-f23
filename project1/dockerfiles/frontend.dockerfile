FROM hamorrar/kvs:base

MAINTAINER Hilal Morrar <hilal@utexas.edu> version: 0.1

USER root

WORKDIR $KVS_HOME

CMD python3 frontend.py
