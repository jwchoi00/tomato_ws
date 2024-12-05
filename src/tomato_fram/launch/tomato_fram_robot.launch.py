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

    TURTLEBOT3_MODEL = "burger"
    # Launch Configuration
    use_sim_time = LaunchConfiguration('use_sim_time')
    # Launch Arguments
    declare_enable_drive = DeclareLaunchArgument(
    'use_sim_time',
    default_value='false',
    description='Use simulation time if true'
    )

    # Paths
    pkg_description = get_package_share_directory('description')
    xacro_file = os.path.join(pkg_description, 'urdf', 'robot_2.xacro')
    rviz_config_file = os.path.join(pkg_description, 'rviz', 'robot.rviz')
    world = os.path.join(
        pkg_description, "worlds", "tomato_fram.world"
    )
    print(world)
    # Process Xacro file
    robot_description = xacro.process_file(xacro_file).toxml()
    
    # Parameters
    params = {
        'ignore_timestamp': False,
        'robot_description': robot_description,
        'use_sim_time': use_sim_time
    }


    # Gazebo Launch
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzserver.launch.py")
        ),
        launch_arguments={"world": world}.items(),
    )
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzclient.launch.py")
        ),
    )

    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(declare_enable_drive)

    # RViz Launch
    RViz_launch  = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        on_exit=Shutdown()
    )
    # Robot State Publisher
    Robot_State_Publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    # Joint State Publisher GUI
    Joint_State_Publisher_GUI = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )
    # Spawn Entity in Gazebo
    Spawn_Entity_in_Gazebo = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        arguments=[
            "-file",
            '/home/g1/multitb_ws/src/turtlebot3_multi_robot/models/turtlebot3_waffle/model.sdf',
            '-entity', 'robot_2',
            '-x', '-2', '-y', '0', '-z', '0.1',
        ],
        output='screen'
    )
    ld.add_action(RViz_launch)
    ld.add_action(Robot_State_Publisher)
    ld.add_action(Joint_State_Publisher_GUI)
    ld.add_action(Spawn_Entity_in_Gazebo)
    # Return Launch Description
    # return LaunchDescription([

    # ])
    return ld