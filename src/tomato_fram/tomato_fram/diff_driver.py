import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class DiffDriveController(Node):
    def __init__(self):
        super().__init__('diff_drive_controller')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.velocity_callback,
            10)
        self.publisher = self.create_publisher(Odometry,'odom',10)
        self.timer = self.create_timer(0.1, self.update_odometry)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

    def velocity_callback(self, msg):
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    def update_odometry(self):
        dt = 0.1 #타이머 주기
        self.x += self.linear_velocity * math.cos(self.theta) * dt
        self.y += self.linear_velocity * math.sin(self.theta) * dt
        self.theta += self.angular_velocity * dt

        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = math.sin(self.theta /2.0)
        odom.pose.pose.orientation.w = math.cos(self.theta / 2.0)
        self.publisher.publish(odom)

def main(args=None):
    rclpy.init(args=args)
    controller = DiffDriveController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()