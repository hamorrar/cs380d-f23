#!/bin/bash

sudo docker image rm $(sudo docker image ls --format '{{.Repository}} {{.ID}}' | grep 'hamorrar' | awk '{print $2}')

cd dockerfiles

sudo docker build . -f base.dockerfile -t hamorrar/kvs:base --network=host
sudo docker push hamorrar/kvs:base

sudo docker build . -f client.dockerfile -t hamorrar/kvs:client --network=host
sudo docker push hamorrar/kvs:client

sudo docker build . -f frontend.dockerfile -t hamorrar/kvs:frontend --network=host
sudo docker push hamorrar/kvs:frontend

sudo docker build . -f server.dockerfile -t hamorrar/kvs:server --network=host
sudo docker push hamorrar/kvs:server

cd ..
