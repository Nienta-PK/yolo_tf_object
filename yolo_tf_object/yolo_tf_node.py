import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy # Added these imports
from yolo_msgs.msg import DetectionArray
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class YoloVisualizerNode(Node):
    def __init__(self):
        super().__init__('yolo_visualizer_node')
        
        # Define QoS to match the YOLO node's Best Effort output
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )
        
        # Subscriber for 3D detections
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/detections_3d',
            self.detection_callback,
            qos_profile 
        )

        self.tf_broadcaster = TransformBroadcaster(self)
        self.marker_pub = self.create_publisher(MarkerArray, '/yolo/box_markers', 10)
        
        self.get_logger().info("YOLO 3D Box Visualizer Started")

    def detection_callback(self, msg: DetectionArray):
        marker_array = MarkerArray()

        for i, det in enumerate(msg.detections):
            center = det.bbox3d.center.position
            size = det.bbox3d.size 

            # 1. Broadcast TF Frame
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = det.bbox3d.frame_id 
            t.child_frame_id = f"object_{det.class_name}_{i}"
            t.transform.translation.x = center.x
            t.transform.translation.y = center.y
            t.transform.translation.z = center.z
            self.tf_broadcaster.sendTransform(t)

            # 2. Create 3D Bounding Box Marker
            marker = Marker()
            marker.header.frame_id = det.bbox3d.frame_id
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "yolo_boxes"
            marker.id = i
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            
            marker.pose.position.x = center.x
            marker.pose.position.y = center.y
            marker.pose.position.z = center.z
            
            marker.scale.x = size.x
            marker.scale.y = size.y
            marker.scale.z = size.z

            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.color.a = 0.5 
            
            marker.lifetime = rclpy.duration.Duration(seconds=0.5).to_msg()
            marker_array.markers.append(marker)

        if marker_array.markers:
            self.marker_pub.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = YoloVisualizerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()