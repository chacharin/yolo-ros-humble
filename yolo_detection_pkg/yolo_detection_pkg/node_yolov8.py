from .mute_c_stderr import mute_c_stderr
mute_c_stderr()            # silence native warnings *now*


import json
from datetime import datetime

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO


class YoloShowAndPublish(Node):
    def __init__(self):
        super().__init__("node_yolov8")

        # Params
        self.declare_parameter("model_name", "yolov8n.pt")
        model_name = self.get_parameter("model_name").get_parameter_value().string_value

        # Model
        self.model = YOLO(model_name)
        self.names = self.model.names  # class-id → label

        # ROS interfaces
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image,
                                            "/camera/image_raw",
                                            self.image_cb,
                                            10)
        self.pub = self.create_publisher(String,
                                         "/yolo_result",
                                         10)

        # OpenCV display window
        cv2.namedWindow("YOLOv8", cv2.WINDOW_NORMAL)
        self.get_logger().info("node_yolov8 ready – showing window ‘YOLOv8’")

    def image_cb(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        dets = self.model(frame, verbose=False)[0]

        output_list = []
        for box in dets.boxes:
            conf = float(box.conf)
            if conf < 0.5:
                continue

            cls_id = int(box.cls)
            label = self.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            # draw rectangle + label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}",
                        (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        1,
                        cv2.LINE_AA)

            # build JSON-serialisable dict
            output_list.append({
                "id": cls_id,
                "label": label,
                "conf": round(conf, 4),
                "x": x1,
                "y": y1,
                "w": w,
                "h": h
            })

        # show the image
        cv2.imshow("YOLOv8", frame)
        cv2.waitKey(1)

        # publish JSON even if empty list (downstream can filter)
        json_msg = String()
        json_msg.data = json.dumps({
            "stamp": msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
            "detections": output_list
        })
        self.pub.publish(json_msg)

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main():
    rclpy.init()
    node = YoloShowAndPublish()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

