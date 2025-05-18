from setuptools import find_packages, setup
from glob import glob

package_name = "yolo_detection_pkg"

setup(
    name=package_name,
    version="0.3.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
         [f"resource/{package_name}"]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Your Name",
    maintainer_email="you@example.com",
    description="Webcam → YOLOv8 (.pt) → JSON detections",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "node_read_cam   = yolo_detection_pkg.node_read_cam:main",
            "node_yolov8     = yolo_detection_pkg.node_yolov8:main",
            "node_read_json  = yolo_detection_pkg.node_read_json:main",
        ],
    },
)

