## Steps to run
1. Run the docker image using 

    `docker run -it --rm -d -p 6080:80 -p 5900:5900 prince/ros-kinetic-desktop:latest`

2. You can access VNC in your browser at `localhost:6080`. You should see a webpage similar to this
![Alt text](images/vnc-desktop.png?raw=true "Title")
3. Then start rrbot gazebo simulation using below command. You must run this comand inside the Lx Terminal in VNC and not in your host terminal.

    `roslaunch rrbot_gazebo rrbot_world.launch`
4. Wait for the simulation to load.
5. Follow instructions at this [link](../rrbot-control/README.md) to control rrbot joint using script.



