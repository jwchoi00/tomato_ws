# tomato_ws

run 하는 법

ros2 launch tomato_fram tomato_fram_robot.launch.py

ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=/home/g1/tomato_ws/src/description/map/new_tomato_map.yaml



20241208 지원 수정 사항

- 카메라 위치 조정 /home/g1/tomato_ws/src/description/models/turtlebot3_waffle/model.sdf
![Screenshot from 2024-12-07 20-35-17](https://github.com/user-attachments/assets/d6005983-f758-4ba3-9013-4dc8f5c9dad6)

- nav2 안전영역 축소 /home/g1/work/turtlebot3_ws/src/turtlebot3/turtlebot3_navigation2/param/waffle.yaml
![Screenshot from 2024-12-07 20-36-34](https://github.com/user-attachments/assets/c36092fc-4ccf-4ca9-b134-27e1d13669dc)


로봇 spawn 하는 법
ros2 run gazebo_ros spawn_entity.py -file <model.sdf가 있는 상대 절대 경로> -entity <이름 설정>

ex) ros2 run gazebo_ros spawn_entity.py -file src/turtlebot3_multi_robot/models/turtlebot3_burger/model.sdf -entity turtlebot1

map 저장시
ros2 launch turtlebot3_cartographer cartographer.launch.py
ros2 run nav2_map_server map_saver_cli -f ~/map


20241208 지원 수정
변경됨 멀티 스폰을 못했기 때문에 기존 것에 load map 변경과 turtlebot 카메라 위치 변경 nav2 yaml 변경
ros2 launch turtlebot3_multi_robot gazebo_multi_nav2_world.launch.py 

로봇을 하나식 컨트롤 하기 위해 tb1, tb2의 namespace로 설정하여 각자 통제

ros2 run tomato_fram tomato_object_detect_tb1
ros2 run tomato_fram tomato_object_detect_tb2

ros2 run tomato_fram tomato_gui_tb1
ros2 run tomato_fram tomato_gui_tb2