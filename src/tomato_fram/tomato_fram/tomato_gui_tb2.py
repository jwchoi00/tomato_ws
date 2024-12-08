import os
import sys
import rclpy
import math
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Pose, Quaternion
from tomato_interfaces.srv import TransportRobot
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile
from PyQt5.QtCore import QTimer

class TransportRobotClass(Node):
    def __init__(self):
        super().__init__('transport_robot')
        
        # Create action client for navigation
        self.action_client = ActionClient(self, NavigateToPose, '/tb2/navigate_to_pose')
        
        # Create subscriber to receive the position of the harvesting robot
        self.position_subscriber = self.create_subscription(
            PoseStamped, '/tb1/odom', self.follow_harvesting_robot_callback, 10
        )
        
        # Create a service client to listen for go home requests
        self.create_service(TransportRobot, '/tb2/go_home', self.go_home_callback)

        
        # State variables
        self.is_moving = False
        self.is_following = False
        self.following_robot_position = None
        target_yaw = 55.0  # Target yaw angle in radians (facing East)
        quaternion = self.create_quaternion_from_yaw(target_yaw)
        # Waypoint for home
        self.home_position = Pose()
        self.home_position.position.x = 0.2
        self.home_position.position.y = -2.7
        self.home_position.orientation = quaternion
        
        # Timer for periodic checks
        self.timer = QTimer(None)
        self.timer.timeout.connect(self.update_following)
        self.timer.start(100)

        self.get_logger().info("Transport robot initialized and ready to follow harvesting robot.")

    def follow_harvesting_robot_callback(self, msg):
        self.following_robot_position = msg.pose
        self.get_logger().info(f"Following robot position: {self.following_robot_position.position.x}, {self.following_robot_position.position.y}")
        self.send_goal(self.following_robot_position.position.x, self.following_robot_position.position.y)

    def create_quaternion_from_yaw(self, yaw):
        """Convert yaw angle (in radians) to quaternion."""
        q = Quaternion()
        q.w = math.cos(yaw / 2)
        q.z = math.sin(yaw / 2)
        q.x = 0.0
        q.y = 0.0
        return q
    def send_goal(self, x, y):
        """
        Send a goal to move the transport robot to the target position.
        """
        target_yaw = -135.0  # Target yaw angle in radians (facing East)
        quaternion = self.create_quaternion_from_yaw(target_yaw)
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.pose.position.x = x + 0.5
        goal_msg.pose.pose.position.y = y + 0.2
        goal_msg.pose.pose.orientation = quaternion

        self.get_logger().info(f"Sending goal to transport robot: {goal_msg.pose.pose.position.x}, {goal_msg.pose.pose.position.y}")
        
        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)
        self.is_moving = True

    def goal_response_callback(self, future):
        """
        Callback for the response of the goal sending.
        """
        goal_handle = future.result()
        if goal_handle is None:
            self.get_logger().error("Goal handle is None!")
            return

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected!")
            return

        self.get_logger().info("Goal accepted!")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        """
        Callback for the result of the navigation goal.
        """
        result = future.result()
        if result.status == 4:  # Goal succeeded
            self.get_logger().info("Transport robot reached target position!")
            self.is_moving = False
        else:
            self.get_logger().error("Failed to reach the target position!")

    def go_home_callback(self, request, response):
        """
        This service is called when the harvesting robot requests the transport robot to go home.
        After reaching home, it will return to the harvesting robot.
        """
        self.gohome = request.gohome
        self.get_logger().info("Transport robot received 'go home' request. Heading home now.")
        self.send_goal(self.home_position.position.x, self.home_position.position.y)

        # Wait for the transport robot to reach home and then send it back to harvesting robot
        self.is_following = False
        response.succeed = True
        return response

    def update_following(self):
        """
        Periodic check to update the following state of the transport robot.
        If the transport robot is not currently moving, it will continue to follow the harvesting robot.
        """
        if self.following_robot_position is not None and not self.is_moving:
            if not self.is_following:
                self.is_following = True
                self.send_goal(self.following_robot_position.position.x, self.following_robot_position.position.y)

def main(args=None):
    rclpy.init(args=args)
    transport_robot = TransportRobotClass()
    rclpy.spin(transport_robot)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
