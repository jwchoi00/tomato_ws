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

    TURTLEBOT3_MODEL = "waffle"
    # Launch Configuration
    # Launch Arguments
    declare_enable_drive = DeclareLaunchArgument(
    'use_sim_time',
    default_value='false',
    description='Use simulation time if true'
    )
    urdf_file_name = "turtlebot3_" + TURTLEBOT3_MODEL + ".urdf"
    # Paths
    pkg_description = get_package_share_directory('description')
    urdf = os.path.join(pkg_description, 'urdf', urdf_file_name)
    rviz_config_file = os.path.join(pkg_description, 'rviz', 'robot.rviz')
    world = os.path.join(
        pkg_description, "worlds", "new_farm_small.world"
    )
    # Process Xacro file
    with open(urdf, 'r') as infp:
        robot_description = infp.read()

    # Parameters
    params = {"use_sim_time": False,
            "publish_frequency": 10.0}


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
        parameters=[params],
        arguments=[urdf]
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
            os.path.join(pkg_description,'models', 'turtlebot3_' + TURTLEBOT3_MODEL, 'model.sdf'),
            '-entity', 'robot_2',
            '-x', '-1', '-y', '-1', '-z', '0.12', "-Y", "0",
        ],
        output='screen'
    )
    # Spawn_Entity_in_Gazebo_2 = Node(
    #     package='gazebo_ros',
    #     executable='spawn_entity.py',
    #     name='spawn_entity',
    #     arguments=[
    #         "-file",
    #         urdf,
    #         '-entity', 'robot_2',
    #         '-x', '-2', '-y', '0', '-z', '0.1', "-Y", "3.14159",
    #     ],
    #     output='screen'
    # )

    ld.add_action(Robot_State_Publisher)
    #ld.add_action(Joint_State_Publisher_GUI)
    ld.add_action(Spawn_Entity_in_Gazebo)
    #ld.add_action(RViz_launch)
    return ld