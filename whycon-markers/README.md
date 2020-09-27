## Run as distributed applciation to detect whycon markers

1. Start `rosmaster` using this:
    
    `docker-compose up rosmaster`
2. Start whycon simulation gazebo using vnc
    
    `docker-compose up -d rrbot-gazebo`
3. Go to `localhost:6080` in your browser and click **Connect**. 

4. Open LXTerminal. 

    a) We will first compile `whycon` pkg as it failed to compile while building image. 

    ```
    cd $OVERLAY_WS
    
    catkin_make -DCATKIN_WHITELIST_PACKAGES="whycon" 
    # Run the above command until the complation is successful
    
    source devel/setup.bash  
    ```

    b) Lets simulate out whycon markers in gazebo. 

    `roslaunch mypkg task_1.launch`
    
    c) Wait for the simulation to render completely.

    d) Once the urdf has been rendered, start the detect_whycon script using:
    `roslaunch mypkg detect_whycon.launch`

    e) You should be able to see the detected markers in the output image.
    ![markers](images/markers.png?raw=true "Markers") 

6. Get the pose data by running the `get_marker_data.py` script.

    `docker exec -it whycon-gazebo /bin/bash -c "rosrun mypkg get_marker_data.py"`