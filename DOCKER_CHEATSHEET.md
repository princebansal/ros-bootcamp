# Docker cheatsheet

## docker
1) Build using `DockerFile`
    
    `docker build -t <repo>/<image>:<tag> . `
2) Run container

    `docker run -it --rm <repo>/<image>:<tag>`
3) Run with env variable

    `docker run -it --rm -e <VARIABLE_NAME>=<VARIABLE_VALUE> <repo>/<image>:<tag>`
4) Run with port forwarding

    `docker run -it --rm -p <host-port>:<container-port> <repo>/<image>:<tag>`
5) List containers

    `docker ps`
6) List all containers including stopped

    `docker ps -a`
7) Stop container

    `docker stop <container-id>`
8) View images

    `docker images`
9) Remove all dangling images

    `docker image rm $(docker images -f "dangling=true" -q)`
10) Remove all stopped containers

    `docker container rm $(docker ps -a -q)`
11) Find networks associated to a container

    `docker inspect -f '{{range $key, $value := .NetworkSettings.Networks}}{{$key}} {{end}}' <container-id>`
12) Find containers in a network

    `docker inspect -f '{{index .Options "com.docker.network.bridge.enable_icc"}}' <network-name>`

## docker-compose
1) Start the services

    `docker-compose up -d <service-name>`
2) Start all services

    `docker-compose up -d`
3) Stop all services

    `docker-compose stop`
4) Find all running services

    `docker-compose ps`
5) Tail logs of service 

    `docker-compose logs -f rosmaster`
6) List networks

    `docker-compose network ls`
7) Build service images

    `docker-compose build`