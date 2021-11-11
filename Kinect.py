import ctypes
import cv2
import os
lib_cv = ctypes.CDLL('C:/Users/anstn/Desktop/KINECT_DLL/Kinect_DLL/packages/opencv/build/x64/vc15/bin/opencv_world453.dll')
libd_cv = ctypes.CDLL('C:/Users/anstn/Desktop/KINECT_DLL/Kinect_DLL/packages/opencv/build/x64/vc15/bin/opencv_world453d.dll')
lib_k4a = ctypes.CDLL('C:/Users/anstn/Desktop/KINECT_DLL/Kinect_DLL/packages/Microsoft.Azure.Kinect.Sensor.1.4.1/lib/native/amd64/release/k4a.dll')
lib_de = ctypes.CDLL('C:/Users/anstn/Desktop/KINECT_DLL/Kinect_DLL/packages/Microsoft.Azure.Kinect.Sensor.1.4.1/lib/native/amd64/release/depthengine_2_0.dll')
lib_k4arec = ctypes.CDLL('C:/Users/anstn/Desktop/KINECT_DLL/Kinect_DLL/packages/Microsoft.Azure.Kinect.Sensor.1.4.1/lib/native/amd64/release/k4arecord.dll')
kinect_lib = ctypes.CDLL('C:/Users/anstn/Desktop/KINECT_DLL/Kinect_DLL/x64/Debug/Kinect_DLL.dll')
