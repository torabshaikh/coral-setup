#!/usr/bin/bash
# ssh-add /.ssh/bitbucket

git clone https://github.com/torabshaikh/coral-setup.git
wget https://github.com/intel-iot-devkit/sample-videos/raw/master/face-demographics-walking-and-pause.mp4

cd coral-setup

sudo docker rm coral
sudo docker build -f Dockerfile -t coral  .
sudo docker run  --name=coral --privileged coral
