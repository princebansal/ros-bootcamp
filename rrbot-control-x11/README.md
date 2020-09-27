## Run as distributed applciation to control rrbot joints

1. Start `rosmaster` using this:
    
    `docker-compose up rosmaster`
2. Start rrbot gazebousing vnc
    
    `docker-compose up -d rrbot-gazebo`
3. Go to `localhost:6080` in your browser and click **Connect**. 

4. Open LXTerminal and start rrbot gazebo service suing this:
    
    `roslaunch rrbot_gazebo rrbot_world.launch`
5. Wait for the rrbot urdf to render completely. 

6. Once the urdf has been rendered, start the rrbot control service using this in you host machine:
    
    `docker-compose up -d rrbot-control`
7. Now run the rrbot-talker to control your robot:
    
    `docker-compose up -d rrbot-talker`
8. You should see the joint moving to the desired position.