import rclpy
from rclpy.node import Node
from yolo_msgs.msg import DetectionArray
from visualization_msgs.msg import Marker, MarkerArray

class Yolo3DBoxNode(Node):
    def __init__(self):
        super().__init__('yolo_3d_box_node')

        self.sub = self.create_subscription(
            DetectionArray,
            '/yolo/detections_3d',
            self.callback,
            10
        )

        self.pub = self.create_publisher(MarkerArray, '/yolo/markers', 10)

    def callback(self, msg: DetectionArray):
        markers = MarkerArray()

        for i, det in enumerate(msg.detections):
            m = Marker()
            m.header.frame_id = det.bbox3d.frame_id  # camera_link
            m.header.stamp = self.get_clock().now().to_msg()

            m.ns = "yolo_3d"
            m.id = i
            m.type = Marker.CUBE
            m.action = Marker.ADD

            # position
            m.pose.position.x = det.bbox3d.center.position.x
            m.pose.position.y = det.bbox3d.center.position.y
            m.pose.position.z = det.bbox3d.center.position.z

            # orientation
            m.pose.orientation.w = 1.0

            # size
            m.scale.x = det.bbox3d.size.x
            m.scale.y = det.bbox3d.size.y
            m.scale.z = det.bbox3d.size.z

            # color (green box)
            m.color.r = 0.0
            m.color.g = 1.0
            m.color.b = 0.0
            m.color.a = 0.6

            markers.markers.append(m)

        self.pub.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = Yolo3DBoxNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()