import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class JsonLogger(Node):
    def __init__(self):
        super().__init__("node_read_json")
        self.sub = self.create_subscription(
            String,
            "/yolo_result",
            self.cb,
            10)

    def cb(self, msg: String):
        data = json.loads(msg.data)
        for det in data["detections"]:
            self.get_logger().info(
                f"{det['label']:<12} conf={det['conf']:.2f}  "
                f"x={det['x']} y={det['y']} w={det['w']} h={det['h']}"
            )


def main():
    rclpy.init()
    node = JsonLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

