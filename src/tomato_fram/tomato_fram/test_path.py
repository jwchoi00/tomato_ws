import os
from ament_index_python.packages import get_package_share_directory

pkg_description = get_package_share_directory('description')
#turtlebot3_multi_robot = get_package_share_directory("turtlebot3_multi_robot")
#TURTLEBOT3_MODEL = "burger"
world = os.path.join(pkg_description, 'urdf', 'robot_2.xacro'),
print(world)