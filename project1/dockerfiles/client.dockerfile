FROM hamorrar/kvs:base

MAINTAINER Hilal Morrar <hilal@utexas.edu> version: 0.1

USER root

WORKDIR $KVS_HOME
ENV PYTHONUNBUFFERED=1

# COPY client.py $KVS_HOME/

CMD python3 client.py -i $CLIENT_ID
