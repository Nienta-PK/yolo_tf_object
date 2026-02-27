import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge

from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker, MarkerArray
from yolo_msgs.msg import DetectionArray


class FastOverlayNode(Node):
    def __init__(self):
        super().__init__('fast_overlay_node')

        self.bridge = CvBridge()
        self.latest_detections = None

        # Fast QoS (low latency)
        self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )

        self.create_subscription(
            DetectionArray,
            '/yolo/detections_3d',
            self.detection_callback,
            10
        )

        self.img_pub = self.create_publisher(Image, '/yolo/fast_dbg_image', 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/yolo/fast_markers', 10)

        self.get_logger().info("Fast YOLO Overlay Node Started")

    def detection_callback(self, msg: DetectionArray):
        self.latest_detections = msg

    def image_callback(self, img_msg: Image):
        if self.latest_detections is None:
            return

        frame = self.bridge.imgmsg_to_cv2(img_msg, 'bgr8')
        markers = MarkerArray()

        for i, det in enumerate(self.latest_detections.detections):
            # --- 2D BOX ---
            cx = det.bbox.center.position.x
            cy = det.bbox.center.position.y
            w = det.bbox.size.x
            h = det.bbox.size.y

            x1 = int(cx - w / 2)
            y1 = int(cy - h / 2)
            x2 = int(cx + w / 2)
            y2 = int(cy + h / 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det.class_name} {det.score:.2f}"
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # --- 3D MARKER ---
            if det.bbox3d.frame_id:
                m = Marker()
                m.header.frame_id = det.bbox3d.frame_id
                m.header.stamp = img_msg.header.stamp
                m.ns = "yolo_3d"
                m.id = i
                m.type = Marker.CUBE
                m.action = Marker.ADD

                m.pose.position.x = det.bbox3d.center.position.x
                m.pose.position.y = det.bbox3d.center.position.y
                m.pose.position.z = det.bbox3d.center.position.z
                m.pose.orientation.w = 1.0

                m.scale.x = det.bbox3d.size.x
                m.scale.y = det.bbox3d.size.y
                m.scale.z = det.bbox3d.size.z

                m.color.r = 0.0
                m.color.g = 1.0
                m.color.b = 0.0
                m.color.a = 0.5

                markers.markers.append(m)

        self.img_pub.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))
        self.marker_pub.publish(markers)


def main():
    rclpy.init()
    node = FastOverlayNode()
    rclpy.spin(node)
    rclpy.shutdown()