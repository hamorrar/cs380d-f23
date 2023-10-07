#!/bin/bash

# sudo docker image rm $(sudo docker image ls --format '{{.Repository}} {{.ID}}' | grep 'hamorrar' | awk '{print $2}')

# cd dockerfiles

sudo docker build . -f dockerfiles/base.dockerfile -t hamorrar/kvs:base --network=host
#sudo docker push hamorrar/kvs:base

sudo docker build . -f dockerfiles/client.dockerfile -t hamorrar/kvs:client --network=host
#sudo docker push hamorrar/kvs:client

sudo docker build . -f dockerfiles/frontend.dockerfile -t hamorrar/kvs:frontend --network=host
#sudo docker push hamorrar/kvs:frontend

sudo docker build . -f dockerfiles/server.dockerfile -t hamorrar/kvs:server --network=host
#sudo docker push hamorrar/kvs:server

cd ..
