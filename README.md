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
