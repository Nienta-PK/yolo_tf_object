from setuptools import setup
import os
from glob import glob

package_name = 'yolo_tf_object'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tata',
    maintainer_email='tata@todo.todo',
    description='Publish TF and 3D visualization for YOLO objects',
    license='TODO',
    entry_points={
        'console_scripts': [
            'yolo_tf_node = yolo_tf_object.yolo_tf_node:main',
            'yolo_marker_node = yolo_tf_object.yolo_marker_node:main',
            'yolo_overlay_node = yolo_tf_object.yolo_overlay_node:main',
        ],
    },
)