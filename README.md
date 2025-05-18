**ติดตั้ง ROS Dependencies**
```
sudo apt update
```
```
sudo apt install -y python3-pip ros-humble-cv-bridge ros-humble-vision-msgs
```

**สร้าง Package**
```
cd ~/ros2_ws/src
```
```
ros2 pkg create --build-type ament_python yolo_detection_pkg --dependencies rclpy sensor_msgs vision_msgs cv_bridge
```
```
cd ~/ros2_ws/
```
```
colcon build --symlink-install
```

**ตั้งตั้ง Python Library**
```
pip install opencv-python ultralytics
```

**Downgrade แก้ปัญหา Numpy**
```
pip uninstall numpy
pip install --upgrade "numpy<2.0,>=1.26.4"
```

**กำหนดตัวแปร แก้ Ulrealytics Auto Online Upgrade**
```
export ULTRALYTICS_NO_AUTOINSTALL=1
```
```
echo 'export ULTRALYTICS_NO_AUTOINSTALL=1' >> ~/.bashrc
```

**Build System**
```
cd ~/ros2_ws/
```
```
colcon build --symlink-install
```

**Full Re - Build**
```
cd ~/ros2_ws
```
```
rm -rf build install log
```
```
colcon build --symlink-install
```

**Launch Project**
```
ros2 launch yolo_detection_pkg yolo_pipeline.launch.py
```


