from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        # YOLO TF broadcaster
        Node(
            package='yolo_tf_object',
            executable='yolo_tf_node',
            name='yolo_tf_node',
            output='screen'
        ),

        # 3D Marker Publisher
        Node(
            package='yolo_tf_object',
            executable='yolo_overlay_node',
            name='yolo_overlay_node',
            output='screen'
        ),
    ])