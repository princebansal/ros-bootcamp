ARG FROM_IMAGE=ros:kinetic-ros-core
#ARG FROM_IMAGE=osrf/ros:kinetic-desktop-full
ARG OVERLAY_WS=/opt/ros/overlay_ws

# multi-stage for caching
FROM $FROM_IMAGE AS cacher

# clone overlay source
ARG OVERLAY_WS
WORKDIR $OVERLAY_WS/src
RUN echo "\
repositories: \n\
  ros-simulation/gazebo_ros_demos: \n\
    type: git \n\
    url: https://github.com/ros-simulation/gazebo_ros_demos.git \n\
    version: kinetic-devel \n\
" > ../overlay.repos
RUN ln -snf /bin/bash /bin/sh 
RUN apt-get update && apt-get -y install python3-vcstool && apt-get -y install git
#RUN /bin/bash -c "source ~/.bashrc"
RUN vcs import ./ < ../overlay.repos
RUN find . -path '*dummy_robot' -type d | \ 
      xargs -n 1 -I {} rm -rf {}
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
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    apt-get update && rosdep init && rosdep update && rosdep install -y \
      --from-paths \
        src/ros-simulation/gazebo_ros_demos \
      --ignore-src \
    && rm -rf /var/lib/apt/lists/*

# build overlay source
COPY --from=cacher $OVERLAY_WS/src ./src
ARG OVERLAY_MIXINS="release"
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    catkin_make 
#	-DCATKIN_WHITELIST_PACKAGES="rrbot_description"

# source entrypoint setup
RUN ls $OVERLAY_WS/
ENV OVERLAY_WS $OVERLAY_WS
#RUN sed --in-place --expression \
#      '$isource "$OVERLAY_WS/devel/setup.bash"' \
#      /ros_entrypoint.sh

RUN sudo apt-get -y update && sudo apt-get -y upgrade

RUN echo "source $OVERLAY_WS/devel/setup.bash" >> /entrypoint.sh
RUN touch /root/bashrc && echo "source $OVERLAY_WS/devel/setup.bash" >> /root/.bashrc
RUN touch ~/.bashrc && echo "source $OVERLAY_WS/devel/setup.bash" >> ~/.bashrc

ENV BASH_ENV "$OVERLAY_WS/devel/setup.bash"

# run launch file
#CMD ["roslaunch", "rrbot_description", "rrbot_rviz.launch"]

