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

    pkg_description = get_package_share_directory('description')
    #nav2 add
    map_file = os.path.join(pkg_description, 'map', 'new_tomato_map.yaml')

    #turtlebot3 Navigation2 Launch
    navigation2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("turtlebot3_navigation2"), "launch", "navigation2.launch.py")
        ),
        launch_arguments={"map": map_file}.items(),
    )

    ld.add_action(navigation2_cmd)
    return ld
