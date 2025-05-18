sudo apt update
sudo apt install -y python3-pip ros-humble-cv-bridge ros-humble-vision-msgs

python3 -m pip install --user opencv-python ultralytics

python3 -m pip install --user --upgrade "numpy<2.0,>=1.26.4"

export ULTRALYTICS_NO_AUTOINSTALL=1
echo 'export ULTRALYTICS_NO_AUTOINSTALL=1' >> ~/.bashrc


mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# drop/clone yolo_detection_pkg here (plus any other packages)
cd ~/ros2_ws
rm -rf build install log        # if rebuilding
colcon build --symlink-install
source install/setup.bash



ros2 launch yolo_detection_pkg yolo_pipeline.launch.py \
      model_name:=yolov8n.pt \
      camera_index:=0 \
      imgsz:=320


