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

from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue

from launch_ros.actions import Node


def generate_launch_description():
    pkg_path = get_package_share_path("aero_hand_open_description")

    left_model_arg = DeclareLaunchArgument(
        name="model",
        default_value=str(pkg_path / "urdf" / "aero_hand_open_left.urdf"),
        description="Absolute path to robot urdf file",
    )

    right_model_arg = DeclareLaunchArgument(
        name="right_model",
        default_value=str(pkg_path / "urdf" / "aero_hand_open_right.urdf"),
        description="Absolute path to right-hand robot urdf file",
    )

    gui_arg = DeclareLaunchArgument(
        name="gui",
        default_value="true",
        choices=["true", "false"],
        description="Flag to enable joint_state_publisher_gui",
    )

    rvizconfig_default = pkg_path / "rviz/config.rviz"

    rvizconfig_arg = DeclareLaunchArgument(
        name="rvizconfig",
        default_value=str(rvizconfig_default),
        description="Absolute path to rviz config file",
    )

    software_rendering_arg = DeclareLaunchArgument(
        name="use_software_rendering",
        default_value="false",
        choices=["true", "false"],
        description="Force RViz to use Mesa software OpenGL for environments without working GPU drivers",
    )

    left_robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]), value_type=str
    )

    right_robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("right_model")]), value_type=str
    )

    ## Nodes
    left_robot_state_publisher_node = Node(
        namespace="left",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[
            {
                "robot_description": left_robot_description,
            }
        ],
    )

    right_robot_state_publisher_node = Node(
        namespace="right",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[
            {
                "robot_description": right_robot_description,
            }
        ],
    )

    left_joint_state_publisher_node = Node(
        namespace="left",
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[{"robot_description": left_robot_description}],
        condition=UnlessCondition(LaunchConfiguration("gui")),
    )

    left_joint_state_publisher_gui_node = Node(
        namespace="left",
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        parameters=[{"robot_description": left_robot_description}],
        condition=IfCondition(LaunchConfiguration("gui")),
    )

    right_joint_state_publisher_node = Node(
        namespace="right",
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[{"robot_description": right_robot_description}],
        condition=UnlessCondition(LaunchConfiguration("gui")),
    )

    right_joint_state_publisher_gui_node = Node(
        namespace="right",
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        parameters=[{"robot_description": right_robot_description}],
        condition=IfCondition(LaunchConfiguration("gui")),
    )

    rviz_node_hardware = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
        condition=UnlessCondition(LaunchConfiguration("use_software_rendering")),
    )

    rviz_node_software = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["--opengl", "210", "-d", LaunchConfiguration("rvizconfig")],
        env={
            "LIBGL_ALWAYS_SOFTWARE": "1",
            "QT_XCB_GL_INTEGRATION": "none",
        },
        condition=IfCondition(LaunchConfiguration("use_software_rendering")),
    )

    left_world_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="left_world_tf",
        arguments=["-0.10", "0", "0", "0", "0", "0", "world", "left_base_link"],
    )

    right_world_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="right_world_tf",
        arguments=["0.10", "0", "0", "0", "0", "0", "world", "right_base_link"],
    )

    return LaunchDescription(
        [
            left_model_arg,
            right_model_arg,
            gui_arg,
            left_joint_state_publisher_gui_node,
            left_joint_state_publisher_node,
            right_joint_state_publisher_gui_node,
            right_joint_state_publisher_node,
            left_robot_state_publisher_node,
            right_robot_state_publisher_node,
            rvizconfig_arg,
            software_rendering_arg,
            rviz_node_hardware,
            rviz_node_software,
            left_world_tf,
            right_world_tf,
        ]
    )
