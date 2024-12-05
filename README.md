# tomato_ws

run 하는 법

ros2 launch tomato_fram tomato_fram_robot.launch.py

로봇 spawn 하는 법
ros2 run gazebo_ros spawn_entity.py -file <model.sdf가 있는 상대 절대 경로> -entity <이름 설정>

ex) ros2 run gazebo_ros spawn_entity.py -file src/turtlebot3_multi_robot/models/turtlebot3_burger/model.sdf -entity turtlebot1
