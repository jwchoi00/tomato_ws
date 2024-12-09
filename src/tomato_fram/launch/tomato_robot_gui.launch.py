import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, Shutdown
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
def generate_launch_description():

    ld = LaunchDescription()

    tomato_gui_tb1 = Node(
            package='tomato_fram',
            executable='tomato_gui_tb1',
            name='tomato_gui_tb1',
            output='screen',
    )
    tomato_gui_tb2 = Node(
            package='tomato_fram',
            executable='tomato_gui_tb2',
            name='tomato_gui_tb2',
            output='screen',
    )
    tomato_object_detect_tb1 = Node(
            package='tomato_fram',
            executable='tomato_object_detect_tb1',
            name='tomato_object_detect_tb1',
            output='screen',
    )
    ld.add_action(tomato_gui_tb1)
    ld.add_action(tomato_gui_tb2)
    ld.add_action(tomato_object_detect_tb1)

    return ld