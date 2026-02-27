# YOLO 3D Object Detection & TF Visualization

This repository provides a ROS 2 package for real-time 3D object detection and coordinate transformation (TF) using **YOLOv8** and **Intel RealSense** cameras. It is designed for robotic assembly tasks, specifically focusing on detecting and locating objects in 3D space for manipulation.

---

## 🛠 Workspace Setup

Follow these steps to clone the dependencies and build the workspace:

```bash
# Create and navigate to workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone dependencies
git clone [https://github.com/realsenseai/realsense-ros.git](https://github.com/realsenseai/realsense-ros.git)
git clone [https://github.com/mgonzs13/yolo_ros.git](https://github.com/mgonzs13/yolo_ros.git)
git clone [https://github.com/Nienta-PK/yolo_tf_object.git](https://github.com/Nienta-PK/yolo_tf_object.git)

# Build the workspace
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash```

---

## 🚀 How to Launch

For the best performance, it is recommended to run these commands in separate terminals.

'''bash
ros2 launch realsense2_camera rs_launch.py \
  rgb_camera.profile:=640x480x30 \
  depth_module.profile:=640x480x30 \
  rgb_camera.qos:=SENSOR_DATA \
  depth_module.qos:=SENSOR_DATA \
  align_depth.enable:=true \
  pointcloud.enable:=true \
  enable_color:=true'''
