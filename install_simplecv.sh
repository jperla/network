#!/bin/sh
sudo pip install http://www.pygame.org/ftp/pygame-1.9.1release.tar.gz
sudo apt-get install libblas-dev
sudo apt-get install liblapack-dev
sudo apt-get install libcv2.1 libcv-dev
sudo pip install scipy
sudo ./prereqs.sh 
sudo pip install https://github.com/ingenuitas/SimpleCV/zipball/master

sudo apt-get install libjpeg-progs libjpeg-dev
sudo apt-get install libjpeg-progs libjpeg-dev
sudo apt-get install libgstreamer-plugins-base0.10-dev

curl -OL http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.3/OpenCV-2.4.3.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fopencvlibrary%2F&ts=1354466268&use_mirror=voxel
bunzip2 OpenCV-2.4.3.tar.bz2 
tar xvf OpenCV-2.4.3.tar 
cd OpenCV-2.4.3/
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D BUILD_EXAMPLES=ON ..
make
sudo make install


sudo chmod a+rw /dev/raw1394

