import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Pose, Quaternion
from tomato_interfaces.srv import TransportRobot
from PyQt5.QtCore import QTimer

class TransportRobotClass(Node):
    def __init__(self):
        super().__init__('transport_robot')

        # Action client for navigation
        self.action_client = ActionClient(self, NavigateToPose, '/tb2/navigate_to_pose')

        # Subscriber for harvesting robot position
        self.create_subscription(
            PoseStamped, '/tb1/odom', self.follow_harvesting_robot_callback, 10
        )

        # Service for 'go home' request
        self.create_service(TransportRobot, '/tb2/go_home', self.go_home_callback)

        # Initialize states and variables
        self.is_moving = False
        self.is_following = True
        self.is_going_home = False
        self.following_robot_position = None
        self.home_position = self.initialize_home_position()

        self.goal_handle = None  # Store the goal_handle here
        
        # Timer for periodic updates
        self.timer = QTimer(None)
        self.timer.timeout.connect(self.update_following)
        self.timer.start(100)

        self.get_logger().info("Transport robot initialized and ready.")

    def initialize_home_position(self):
        """Define the home position."""
        pose = Pose()
        pose.position.x = 0.2
        pose.position.y = -1.3
        pose.orientation = self.create_quaternion_from_yaw(55.0)
        return pose

    def create_quaternion_from_yaw(self, yaw):
        """Convert yaw angle (in radians) to a quaternion."""
        q = Quaternion()
        q.w = math.cos(yaw / 2)
        q.z = math.sin(yaw / 2)
        return q

    def follow_harvesting_robot_callback(self, msg):
        """Callback for harvesting robot position updates."""
        if not self.is_following or self.is_moving or self.is_going_home:
            
            return
        self.following_robot_position = msg.pose
        self.get_logger().info(f"Harvesting robot at: ({msg.pose.position.x}, {msg.pose.position.y})")
        self.send_goal(msg.pose.position.x, msg.pose.position.y)

    def send_goal(self, x, y):
        """Send navigation goal to the transport robot."""
        if self.is_moving:
            self.cancel_current_goal()
            return

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.pose.position.x = x + 0.5
        goal_msg.pose.pose.position.y = y + 0.2
        goal_msg.pose.pose.orientation = self.create_quaternion_from_yaw(-135.0)

        self.get_logger().info(f"Sending goal: ({goal_msg.pose.pose.position.x}, {goal_msg.pose.pose.position.y})")
        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)
        self.is_moving = True

    def goal_response_callback(self, future):
        """Handle response after sending a navigation goal."""
        goal_handle = future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().info("Goal rejected!")
            self.is_moving = False
            return

        self.get_logger().info("Goal accepted.")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        """Handle the result of the navigation goal."""
        result = future.result()
        if result.status == 4:  # Goal succeeded
            self.get_logger().info("Target reached successfully.")
            if self.is_going_home:
                self.get_logger().info("Transport robot is now at home.")
                self.is_going_home = False
        else:
            self.get_logger().error("Failed to reach the target position.")

        self.is_moving = False
        if not self.is_going_home:
            self.is_following = True

    def go_home_callback(self, request, response):
        """Handle 'go home' service request."""
        if self.is_moving:
            self.cancel_current_goal()

        self.get_logger().info("Received 'go home' request. Heading home.")
        self.is_following = False
        self.is_going_home = True
        self.send_goal(self.home_position.position.x, self.home_position.position.y)

        response.succeed = True
        return response

    def cancel_current_goal(self):
        """
        Cancels the current goal to allow new priorities.
        """
        if self.is_moving and self.goal_handle:
            self.get_logger().info("Sending cancel request for the current goal.")
            cancel_future = self.action_client._cancel_goal_async(self.goal_handle)  # Pass goal_handle here
            cancel_future.add_done_callback(self.cancel_callback)
        else:
            self.get_logger().warning("No goal to cancel.")

    def cancel_callback(self, future):
        try:
            cancel_result = future.result()
            if cancel_result.goals_cancelled:
                self.get_logger().info("Current goal cancelled.")
            else:
                self.get_logger().warning("No goals were cancelled.")
        except Exception as e:
            self.get_logger().error(f"Error while cancelling goal: {e}")

    def update_following(self):
        """Periodic updates for following state."""
        if not self.is_following or self.is_moving or not self.following_robot_position:
            return
        self.send_goal(self.following_robot_position.position.x, self.following_robot_position.position.y)

def main(args=None):
    rclpy.init(args=args)
    transport_robot = TransportRobotClass()
    rclpy.spin(transport_robot)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
