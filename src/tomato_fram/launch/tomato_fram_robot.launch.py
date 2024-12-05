import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, Shutdown, RegisterEventHandler
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition

def generate_launch_description():

    ld = LaunchDescription()

    robots = [
    {'name': 'tb1', 'x_pose': '-1.5', 'y_pose': '-0.5', 'z_pose': 0.01},
    # {'name': 'tb2', 'x_pose': '-1.5', 'y_pose': '0.5', 'z_pose': 0.01},
    #{'name': 'tb3', 'x_pose': '1.5', 'y_pose': '-0.5', 'z_pose': 0.01},
    #{'name': 'tb4', 'x_pose': '1.5', 'y_pose': '0.5', 'z_pose': 0.01},
    # ...
    # ...
    ]
    TURTLEBOT3_MODEL = "waffle"

    pkg_description = get_package_share_directory('description')
    rviz_description = get_package_share_directory('turtlebot3_description')

    # Launch Configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time', default_value=use_sim_time, description='Use simulator time'
    )

    enable_drive = LaunchConfiguration('enable_drive', default='false')
    declare_enable_drive = DeclareLaunchArgument(
        name='enable_drive', default_value=enable_drive, description='Enable robot drive node'
    )

    enable_rviz = LaunchConfiguration('enable_rviz', default='true')
    declare_enable_rviz = DeclareLaunchArgument(
        name='enable_rviz', default_value=enable_rviz, description='Enable rviz launch'
    )

    urdf_file_name = "turtlebot3_" + TURTLEBOT3_MODEL + ".urdf"

    urdf = os.path.join(
        rviz_description, "urdf", urdf_file_name
    )
        # Path to the new RViz2 configuration file
    rviz_config_file = os.path.join(pkg_description, 'rviz', 'turtlebot.rviz')

    # Paths
    xacro_file = os.path.join(pkg_description, 'urdf', 'turtlebot3_waffle.urdf')

    # rviz_config_file = os.path.join(pkg_description, 'rviz', 'robot.rviz')

    world = os.path.join(
        pkg_description, "worlds", "tomato_fram.world"
    )

    # Process Xacro file
    with open(xacro_file, 'r') as infp:
        robot_description = infp.read()

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
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_enable_rviz)

    last_action = None

    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]

    last_action = None
    # Spawn turtlebot3 instances in gazebo
    for robot in robots:

        namespace =  '/' + robot['name']

            # Create state publisher node for that instance
        turtlebot_state_publisher = Node(
            package="robot_state_publisher",
            namespace=namespace,
            executable="robot_state_publisher",
            output="screen",
            parameters=[params],
            remappings=remappings,
            arguments=[urdf],
        )
        # Create spawn call
        spawn_turtlebot3 = Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=[
                "-file",
                os.path.join(pkg_description,'models', 'turtlebot3_' + TURTLEBOT3_MODEL, 'model.sdf'),
                "-entity",
                robot['name'],
                "-robot_namespace",
                namespace,
                '-x', robot['x_pose'], '-y', robot['y_pose'],
            '-z', '0.01', '-Y', '0.0',
            '-unpause',
            ],
            output="screen",
        )
        if last_action is None:
            # Call add_action directly for the first robot to facilitate chain instantiation via RegisterEventHandler
            ld.add_action(turtlebot_state_publisher)
            ld.add_action(spawn_turtlebot3)
        else:
            # Use RegisterEventHandler to ensure next robot creation happens only after the previous one is completed.
            # Simply calling ld.add_action for spawn_entity introduces issues due to parallel run.
            spawn_turtlebot3_event = RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=last_action,
                    on_exit=[spawn_turtlebot3,
                            turtlebot_state_publisher],
                )
            )
            ld.add_action(spawn_turtlebot3_event)

            # Save last instance for next RegisterEventHandler
        last_action = spawn_turtlebot3

    for robot in robots:
        namespace =  '/' + robot['name']
        # RViz2 Node
        RViz_launch = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file],
            condition=IfCondition(enable_rviz)
        )
        ld.add_action(RViz_launch)


    return ld
