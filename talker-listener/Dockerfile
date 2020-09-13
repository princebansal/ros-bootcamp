ARG FROM_IMAGE=ros:kinetic-ros-core
ARG OVERLAY_WS=/opt/ros/overlay_ws

# multi-stage for caching
FROM $FROM_IMAGE AS cacher

# clone overlay source
ARG OVERLAY_WS
WORKDIR $OVERLAY_WS/src
RUN ln -snf /bin/bash /bin/sh 

#Copy source from host packages
RUN catkin_create_pkg mypkg
COPY ./mypkg/* mypkg/
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
  apt-get update && \
  sudo apt-get install -y build-essential && \
  sudo apt-get install -y g++ && \
  rosdep init && \
  rosdep update && \
  rosdep install -y \
  --from-paths \
  src/mypkg \
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

RUN sed --in-place --expression \
  '$isource "$OVERLAY_WS/devel/setup.bash"' \
  /ros_entrypoint.sh

ENV BASH_ENV "$OVERLAY_WS/devel/setup.bash"

