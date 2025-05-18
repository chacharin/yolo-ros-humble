from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share   = get_package_share_directory("yolo_detection_pkg")
    default_yaml = os.path.join(pkg_share, "config", "cam_and_model.yaml")

    return LaunchDescription([
        # ---------- CLI-overridable arguments ----------
        DeclareLaunchArgument("camera_index", default_value="0",
                              description="USB-camera index"),
        DeclareLaunchArgument("model_name",  default_value="yolov8n.pt",
                              description="Ultralytics PT model file"),
        DeclareLaunchArgument("imgsz",       default_value="320",
                              description="Network input resolution"),

        # ---------- camera node ----------
        Node(
            package="yolo_detection_pkg",
            executable="node_read_cam",
            name="node_read_cam",
            parameters=[default_yaml, {
                "camera_index": LaunchConfiguration("camera_index"),
            }],
            output="screen",
        ),

        # ---------- YOLO node (.pt backend) ----------
        Node(
            package="yolo_detection_pkg",
            executable="node_yolov8",
            name="node_yolov8",
            parameters=[default_yaml, {
                "model_name": LaunchConfiguration("model_name"),
                "imgsz":      LaunchConfiguration("imgsz"),
            }],
            output="screen",
        ),

        # ---------- JSON logger ----------
        Node(
            package="yolo_detection_pkg",
            executable="node_read_json",
            name="node_read_json",
            output="screen",
        ),
    ])

