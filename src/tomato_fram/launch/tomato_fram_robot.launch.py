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
    world = os.path.join(pkg_description, "worlds", "new_farm_small_bricks.world")

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
    RViz_launch = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        on_exit=Shutdown()
    )

    # Robot State Publisher with Unique Namespaces
    robot_state_namespace_1 = 'robot_1'
    robot_state_namespace_2 = 'robot_2'

    # Robot_State_Publisher_1 = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     name='robot_state_publisher_1',
    #     namespace=robot_state_namespace_1,
    #     output='screen',
    #     parameters=[params, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
    #     arguments=[urdf]
    # )

    # Robot_State_Publisher_2 = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     name='robot_state_publisher_2',
    #     namespace=robot_state_namespace_2,
    #     output='screen',
    #     parameters=[params, {'use_sim_time': LaunchConfiguration('use_sim_time')}],
    #     arguments=[urdf]
    # )

    # Joint State Publisher GUI
    Joint_State_Publisher_GUI = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

        # Spawn Entity for Robot 1
    Spawn_Entity_Robot_1 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity_robot_1',
        namespace='robot_1',
        arguments=[
            "-file",
            os.path.join(pkg_description, 'models', 'turtlebot3_' + TURTLEBOT3_MODEL, 'model.sdf'),
            '-entity', 'robot_1',
            '-x', '-1', '-y', '-1', '-z', '0.12', "-Y", "0",
            '-unpause',
        ],
        output='screen'
    )

    # Spawn Entity for Robot 2
    Spawn_Entity_Robot_2 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity_robot_2',
        namespace='robot_2',
        arguments=[
            "-file",
            os.path.join(pkg_description, 'models', 'turtlebot3_' + TURTLEBOT3_MODEL, 'model.sdf'),
            '-entity', 'robot_2',
            '-x', '-1', '-y', '0', '-z', '0.1', "-Y", "3.14159",
            '-unpause',
        ],
        output='screen'
    )

    # Robot State Publisher for Robot 1
    Robot_State_Publisher_Robot_1 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_robot_1',
        namespace='robot_1',
        output='screen',
        parameters=[params],
        arguments=[urdf],
        remappings=[('/tf', 'robot_1/tf'), ('/tf_static', 'robot_1/tf_static')]
    )

    # Robot State Publisher for Robot 2
    Robot_State_Publisher_Robot_2 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_robot_2',
        namespace='robot_2',
        output='screen',
        parameters=[params],
        arguments=[urdf],
        remappings=[('/tf', 'robot_2/tf'), ('/tf_static', 'robot_2/tf_static')]
    )


    ld.add_action(Robot_State_Publisher_Robot_1)
    #ld.add_action(Robot_State_Publisher_Robot_2)
    ld.add_action(Spawn_Entity_Robot_1)
    #ld.add_action(Spawn_Entity_Robot_2)

    # # Controllers for each robot (Optional)
    # robot_1_controller = Node(
    #     package='controller_manager',
    #     executable='ros2_control_node',
    #     name='robot_1_control',
    #     namespace=robot_state_namespace_1,  # Ensure it's namespaced properly
    #     parameters=[{"robot_description": robot_description}],
    #     output='screen'
    # )

    # robot_2_controller = Node(
    #     package='controller_manager',
    #     executable='ros2_control_node',
    #     name='robot_2_control',
    #     namespace=robot_state_namespace_2,  # Ensure it's namespaced properly
    #     parameters=[{"robot_description": robot_description}],
    #     output='screen'
    # )

    # Add actions to the launch description
    # ld.add_action(Joint_State_Publisher_GUI)
    # ld.add_action(RViz_launch)
    # ld.add_action(robot_1_controller)
    # ld.add_action(robot_2_controller)

    return ld
