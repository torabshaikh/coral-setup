FROM ubuntu:20.04 
WORKDIR /coral-detect

RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get install -y git 
RUN apt-get install -y wget
RUN apt-get install -y curl

RUN apt-get install -y build-essential cmake
RUN apt-get install -y libopenblas-dev liblapack-dev 
RUN apt-get install -y python3.7 python3.7-dev  python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 20 
RUN python -m pip install pip --upgrade
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get -y update
RUN python -m pip install numpy
RUN apt-get install -y libgtk2.0-dev pkg-config libgl1-mesa-glx
RUN apt-get install -y libedgetpu1-std
RUN apt-get install -y python3-edgetpu
RUN dpkg -L python3-edgetpu
RUN pip install pillow --upgrade
RUN pip install opencv-python
RUN pip install opencv-contrib-python
RUN pip install imutils
RUN ls ../
RUN git clone https://github.com/torabshaikh/coral-setup.git
WORKDIR /coral-detect/coral-setup
RUN wget https://github.com/intel-iot-devkit/sample-videos/raw/master/face-demographics-walking-and-pause.mp4
RUN mkdir model
RUN wget https://dl.google.com/coral/canned_models/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite -O model/face_detection.tflite

CMD [ "python", "-u", "detect-no-gui.py"]
