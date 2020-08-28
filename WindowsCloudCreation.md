# Creating Cloud MQTT Broker Using C++ and Windows
## Works on Mac as well
#### https://github.com/eclipse/paho.mqtt.cpp

#### 1. Download CMake GUI v3.5 or newer and Visual Studio 2015 or newer
#### 2. Install the Paho MQTT C library
##### Download library Directly from Site
###### https://projects.eclipse.org/projects/iot.paho/downloads
##### Build from the source using mainline
###### Windows
To build
```
mkdir build.paho

cd build.paho

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" x64

cmake -G "NMake Makefiles" -DPAHO_WITH_SSL=TRUE -DPAHO_BUILD_DOCUMENTATION=FALSE -DPAHO_BUILD_SAMPLES=TRUE -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE=TRUE ..

nmake
```

To install
```
C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin
```
###### Mac/Linux
To build
```
git clone https://github.com/eclipse/paho.mqtt.c.git
cd org.eclipse.paho.mqtt.c.git
make
```
To install
```
sudo make install
```
