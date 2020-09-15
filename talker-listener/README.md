## Run the service using rosmaster
Run the following command to up the services

`docker compose up -d`

Check the listener logs using 

`tail -f log/listener/listener*.log`

## Run the service using launch file
Run the following command to run the service

`docker run -it --rm -d -v $(pwd)/log/talker-listener:/root/.ros/log prince/ros-talker-listener:latest bash -c "roslaunch mypkg launch_talker_listener.launch"
`

Check the listener logs using 

`tail -f log/talker-listener/**/listener*.log`