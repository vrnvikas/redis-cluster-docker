# Docker Redis Cluster

This repository is about Redis Cluster. The following implementation
creates a cluster with 3 master and 1 replica for each master.

## Redis nodes

The cluster is 6 redis instances running with 3 master & 3 slaves, one slave for each master. They run on ports 7001 to 7006.

## Usage

To build your own image run:

Build initializer image:
	
	cd redis-cluster-initializer
    docker build -t redis-cluster-initializer .

Build node image:

    cd redis-cluster-node
    docker build -t redis-cluster-node .

Run project:

    docker-compose up -d

## Environment Variables

| Environment variable 			| Description 																|
| ------------------------------|---------------------------------------------------------------------------|
| `COMPOSE_PROJECT_NAME`        |    Need by python script to form container name 							|
| `REDIS_NODES`                 |    Nodes to add in cluster(docker service name) 							|
| `REDIS_NODE_PORTS`  			|    Port for each node(should match node sequence) 						|			
| `REDIS_NETWORK`  				|    Network name. Needed by python script to extract nodes ip 				| 