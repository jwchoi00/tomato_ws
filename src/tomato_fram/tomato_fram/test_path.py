import os
from ament_index_python.packages import get_package_share_directory

pkg_description = get_package_share_directory('tomato_fram')
turtlebot3_multi_robot = get_package_share_directory("turtlebot3_multi_robot")
TURTLEBOT3_MODEL = "burger"
world = os.path.join(turtlebot3_multi_robot,'models', 'turtlebot3_' + TURTLEBOT3_MODEL, 'model.sdf'),
print(world)