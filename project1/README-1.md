# Project 1

## Design
The system is fully replicated - every server holds the same and complete KVS. So it is tolerant to N-1 failures. The frontend does not store any KV pairs.

### Frontend
The frontend handles most of the logic for the system. Although ineffecient for now, the system shares a single lock so it can be thread safe. There were problems with modifying the membership list while iterating over it, so I made a new list of servers to delete if there was any exception/error while calling, get, put, addServer, and listServer. The crash/failure detection mechanism is if there is any exception raised while making a request to a server, that server is removed from the membership list.

### Server
Each server holds its own KVS. There is basic functionality, but most of the logic is handled by the frontend.

## Directions to run
Same directions to run as the cluster.md file. I reverted all my changes and tested that the system still works. Docker images are pushed to Docker Hub (hamorrar/kvs).

delete_pods.sh, clean_docker_build.sh, python3 run_cluster.py (args).