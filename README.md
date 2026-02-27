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
source install/setup.bash
```

---

## 🚀 How to Launch

For the best performance, it is recommended to run these commands in separate terminals.

### 1. Activate Depth Camera

Starts the RealSense node with optimized QoS settings for low-latency streaming.

```bash
ros2 launch realsense2_camera rs_launch.py \
  rgb_camera.profile:=640x480x30 \
  depth_module.profile:=640x480x30 \
  rgb_camera.qos:=SENSOR_DATA \
  depth_module.qos:=SENSOR_DATA \
  align_depth.enable:=true \
  pointcloud.enable:=true \
  pointcloud.texture_stream:=RS2_STREAM_ANY \
  enable_color:=true
```

### 2. YOLO 3D Detection

Launches the YOLO inference engine. Note the image_reliability:=2 which matches the camera's SENSOR_DATA (Best Effort).

```bash
ros2 launch yolo_bringup yolo.launch.py \
  model:=3rd_model.pt \
  use_3d:=True \
  half:=True \
  fuse_model:=True \
  use_debug:=True \
  target_frame:=camera_link \
  imgsz_width:=416 \
  imgsz_height:=416 \
  image_reliability:=2 \
  depth_image_reliability:=2 \
  depth_info_reliability:=2 \
  input_image_topic:=/camera/camera/color/image_raw \
  input_depth_topic:=/camera/camera/aligned_depth_to_color/image_raw \
  input_depth_info_topic:=/camera/camera/depth/camera_info
```

### 3.Object TF + Visualization Markers

Launches the custom processing node that translates YOLO detections into dynamic TF frames and 3D bounding boxes.

```bash
ros2 launch yolo_tf_object yolo_visualization.launch.py
```

### 4.Visualization

To see the results, open **rviz2** and configure the following displays:

| Display Type | Topic / Setting | Description |
| :--- | :--- | :--- |
| **Global Options** | **Fixed Frame:** `camera_link` | Aligns all data to the camera sensor. |
| **PointCloud2** | `/camera/camera/depth/color/points` | Shows the 3D environment. |
| **TF** | (All enabled) | Shows the dynamic frames for detected objects. |
| **Image** | `/yolo/dbg_image` | Shows RGB feed with 2D bounding boxes. |
| **MarkerArray** | `/yolo/box_markers` | Renders the 3D bounding boxes on the grid. |

> **Note:** Ensure the **Reliability Policy** for the Image and MarkerArray displays is set to **Best Effort** in the RViz sidebar.

