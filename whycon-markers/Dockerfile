ARG FROM_IMAGE=ct2034/vnc-ros-kinetic-full
ARG OVERLAY_WS=/opt/ros/overlay_ws

# multi-stage for caching
FROM $FROM_IMAGE AS cacher

# clone overlay source
ARG OVERLAY_WS
WORKDIR $OVERLAY_WS/src
RUN echo "\
repositories: \n\
  geometry2: \n\
    type: git \n\
    url: https://github.com/ros/geometry2.git \n\
    version: melodic-devel \n\
  brics_actuator: \n\
    type: git \n\
    url: https://github.com/wnowak/brics_actuator.git \n\
    version: master \n\
  eyantra_drone: \n\
    type: git \n\
    url: https://github.com/simmubhangu/eyantra_drone.git \n\
    version: master \n\
  whycon: \n\
    type: git \n\
    url: https://github.com/lrse/whycon.git \n\
    version: master \n\
" > ../overlay.repos
#RUN ln -snf /bin/bash /bin/sh 
RUN apt-get update && apt-get -y install python3-vcstool 
#RUN /bin/bash -c "source ~/.bashrc"
RUN vcs import ./ < ../overlay.repos

RUN catkin_create_pkg mypkg
COPY ./mypkg mypkg/
# copy manifests for caching
WORKDIR /opt
RUN mkdir -p /tmp/opt && \
    find . -name "package.xml" | \
      xargs cp --parents -t /tmp/opt && \
    find ./ -name "COLCON_IGNORE" | \
      xargs cp --parents -t /tmp/opt || true

# multi-stage for building
FROM $FROM_IMAGE AS builder

# install overlay dependencies
ARG OVERLAY_WS
WORKDIR $OVERLAY_WS
COPY --from=cacher /tmp/$OVERLAY_WS/src ./src
RUN sudo apt-get -y update && sudo apt-get -y upgrade
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    rosdep update && rosdep install -y \
    --from-paths \
      src/ \
    --ignore-src \
    && rm -rf /var/lib/apt/lists/*

# build overlay source
COPY --from=cacher $OVERLAY_WS/src ./src
ARG OVERLAY_MIXINS="release"
#RUN wget http://security.ubuntu.com/ubuntu/pool/main/libx/libxslt/xsltproc_1.1.26-8ubuntu1_amd64.deb -o /tmp/ && \
  
RUN apt-get -y update
RUN sudo apt-get install -y libavcodec-dev libsdl2-dev xsltproc \
 libbullet-dev libsdl1.2-dev libgoogle-glog-dev protobuf-compiler \
 python-wstool python-catkin-tools ros-kinetic-mav-msgs ros-kinetic-mavros \ 
 ros-kinetic-octomap-* ros-kinetic-geographic-msgs libgeographic-dev

#Install gazebo 7.17
RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
 wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
 sudo apt-get update && \
 sudo apt-get install gazebo7 -y


RUN . /opt/ros/$ROS_DISTRO/setup.sh && catkin_make -DCATKIN_WHITELIST_PACKAGES="geometry2" && \
 catkin_make -DCATKIN_WHITELIST_PACKAGES="brics_actuator" && \
 catkin_make -DCATKIN_WHITELIST_PACKAGES="eyantra_drone"
# catkin_make -DCATKIN_WHITELIST_PACKAGES="whycon"

#Copy models to gazebo
RUN mkdir -p /root/.gazebo/models && \
    cp -r src/mypkg/src/models/whycon_marker /root/.gazebo/models


# source entrypoint setup
RUN ls $OVERLAY_WS/
ENV OVERLAY_WS $OVERLAY_WS
#RUN sed --in-place --expression \
#      '$isource "$OVERLAY_WS/devel/setup.bash"' \
#      /ros_entrypoint.sh



RUN echo "source $OVERLAY_WS/devel/setup.bash" >> /startup.sh
RUN touch /root/bashrc && echo "source $OVERLAY_WS/devel/setup.bash" >> /root/.bashrc
RUN touch ~/.bashrc && echo "source $OVERLAY_WS/devel/setup.bash" >> ~/.bashrc

ENV BASH_ENV "$OVERLAY_WS/devel/setup.bash"

# run launch file
#CMD ["roslaunch", "rrbot_description", "rrbot_rviz.launch"]

