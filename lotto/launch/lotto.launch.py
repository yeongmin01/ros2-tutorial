#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():


    launch_description = LaunchDescription()

    random_number_node = Node(
        package='lotto',
        executable='random_number',
        name='random_number',
        output='screen')

    winning_checker_node = Node(
        package='lotto',
        executable='winning_checker',
        name='winning_checker',
        output='screen')
    
    launch_description.add_action(winning_checker_node)
    launch_description.add_action(random_number_node)

    return launch_description
