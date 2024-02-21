#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    param_dir = LaunchConfiguration(
        'param_dir',
        default=os.path.join(
            get_package_share_directory('topic_service_action_rclcpp_example'),
            'param',
            'arithmetic_config.yaml'))

    launch_description = LaunchDescription()

    launch_description.add_action(DeclareLaunchArgument(
        'param_dir',
        default_value=param_dir,
        description='Full path of parameter file'))

    argument_node = Node(
        package='topic_service_action_rclcpp_example',
        executable='argument',
        name='argument',
        parameters=[param_dir],
        output='screen')

    operator_node = Node(
        package='topic_service_action_rclcpp_example',
        executable='operator',
        name='operator',
        parameters=[param_dir],
        output='screen')

    checker_node = Node(
        package='topic_service_action_rclcpp_example',
        executable='checker',
        name='checker',
        parameters=[param_dir],
        output='screen')

    calculator_node = Node(
        package='topic_service_action_rclcpp_example',
        executable='calculator',
        name='calculator',
        parameters=[param_dir],
        output='screen')

    launch_description.add_action(argument_node)
    launch_description.add_action(operator_node)
    launch_description.add_action(checker_node)
    launch_description.add_action(calculator_node)

    return launch_description

# def generate_launch_description():
#     param_dir = LaunchConfiguration(
#         'param_dir',
#         default=os.path.join(
#             get_package_share_directory('topic_service_action_rclpy_example'),
#             'param',
#             'arithmetic_config.yaml'))

#     return LaunchDescription([
#         DeclareLaunchArgument(
#             'param_dir',
#             default_value=param_dir,
#             description='Full path of parameter file'),

#         Node(
#             package='topic_service_action_rclpy_example',
#             executable='argument',
#             name='argument',
#             parameters=[param_dir],
#             output='screen',
#             remappings=[
#                 ('/arithmetic_argument', '/argument')]), #[[기존의 Topic name : arithmetic_argument -> argument 로 변경]]


#         Node(
#             package='topic_service_action_rclpy_example',
#             executable='calculator',
#             name='calculator',
#             parameters=[param_dir],
#             output='screen'),
#     ])