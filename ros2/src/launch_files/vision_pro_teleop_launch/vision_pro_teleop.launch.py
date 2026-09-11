# Copyright 2025 Chestnut Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    ## Set the ports for the right and left hands here.
    ## If you want to use only one hand, set the other port to ''
    ## To find the port for your hand on Linux, you can use the command:
    ##   ls /dev/serial/by-id/
    ## Example port: /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A9J6J4J3-if00-port0
    # Defaults (can be overridden from CLI via launch arguments, e.g. `vision_pro_ip:=...`)
    default_right_hand_port = "auto"  # auto detect port
    default_left_hand_port = ""  # no port specified will not initialize the left hand
    default_baudrate = "921600"
    default_feedback_frequency = "100.0"  # Hz
    default_vision_pro_ip = "192.168.1.101"
    default_vision_pro_viz = "true"

    right_hand_port = LaunchConfiguration("right_hand_port")
    left_hand_port = LaunchConfiguration("left_hand_port")
    baudrate = LaunchConfiguration("baudrate")
    feedback_frequency = LaunchConfiguration("feedback_frequency")
    vision_pro_ip = LaunchConfiguration("vision_pro_ip")
    vision_pro_viz = LaunchConfiguration("vision_pro_viz")

    vision_pro_publisher = Node(
        package="apple_vision_pro_mocap",
        executable="apple_vision_data_publisher",
        name="apple_vision_data_publisher",
        output="screen",
        emulate_tty=True,
        parameters=[
            {
                "ip": vision_pro_ip,
                "viz": ParameterValue(vision_pro_viz, value_type=bool),
            }
        ],
    )

    vision_pro_retargeting = Node(
        package="aero_hand_open_retargeting",
        executable="apple_vision_pro_retargeting",
        name="apple_vision_pro_retargeting",
        output="screen",
        emulate_tty=True,
    )

    aero_hand_node = Node(
        package="aero_hand_open",
        executable="aero_hand_node",
        name="aero_hand_node",
        output="screen",
        emulate_tty=True,
        parameters=[
            {
                "right_port": right_hand_port,
                "left_port": left_hand_port,
                "baudrate": ParameterValue(baudrate, value_type=int),
                "feedback_frequency": ParameterValue(feedback_frequency, value_type=float),
            }
        ],
    )

    # Get the path to the RViz config file
    rviz_config_path = os.path.join(
        get_package_share_directory("apple_vision_pro_mocap"),
        "rviz",
        "vision_pro_config.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
        output="screen",
        condition=IfCondition(
            PythonExpression(["'", vision_pro_viz, "' == 'true'"])
        ),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "vision_pro_ip",
                default_value=default_vision_pro_ip,
                description="IPv4 address of the Apple Vision Pro running Tracking Streamer.",
            ),
            DeclareLaunchArgument(
                "vision_pro_viz",
                default_value=default_vision_pro_viz,
                description="Whether to visualize incoming Vision Pro hand tracking data (true/false).",
            ),
            DeclareLaunchArgument(
                "right_hand_port",
                default_value=default_right_hand_port,
                description="Serial port for right hand (or 'auto' to auto-detect).",
            ),
            DeclareLaunchArgument(
                "left_hand_port",
                default_value=default_left_hand_port,
                description="Serial port for left hand (empty string disables left hand).",
            ),
            DeclareLaunchArgument(
                "baudrate",
                default_value=default_baudrate,
                description="Serial baudrate for hand(s).",
            ),
            DeclareLaunchArgument(
                "feedback_frequency",
                default_value=default_feedback_frequency,
                description="Hand feedback frequency in Hz.",
            ),
            vision_pro_publisher,
            vision_pro_retargeting,
            aero_hand_node,
            rviz_node,
        ]
    )
