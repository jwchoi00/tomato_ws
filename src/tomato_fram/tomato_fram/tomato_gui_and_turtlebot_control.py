import os
import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from cv_bridge import CvBridge
import numpy as np

# UI file path
script_dir = os.path.dirname(os.path.realpath(__file__))
ui_file_path = os.path.join(script_dir, 'tomato.ui')
form_class = uic.loadUiType(ui_file_path)[0]


class VideoPlayer(QMainWindow, form_class, Node):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setupUi(self)
        Node.__init__(self, 'video_player')
        self.image_subscription = self.create_subscription(
            Image, '/tomato/image', self.image_callback, 10
        )

        self.action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(30)
        self.latest_frame = None
        self.bridge = CvBridge()

        self.led_indicator = self.findChild(QWidget, "led_indicator")
        self.start_button = self.findChild(QPushButton, "start_button")
        self.start_button.clicked.connect(self.send_goal)

        self.return_button = self.findChild(QPushButton, "return_button")
        self.return_button.clicked.connect(self.return_home)

        self.is_moving = False
        self.tomato_detected = False

    def image_callback(self, msg):
        try:
            cv_image = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, 3)
            qt_image = QImage(cv_image.data, msg.width, msg.height, QImage.Format_RGB888)
            self.latest_frame = qt_image
        except Exception as e:
            self.get_logger().error(f"Error updating image: {e}")

    def update_gui(self):
        if self.latest_frame is not None:
            self.findChild(QLabel, "label_image").setPixmap(QPixmap.fromImage(self.latest_frame))

        # Update LED color based on movement state
        if self.tomato_detected:
            self.led_indicator.setStyleSheet("background-color: yellow;")
        elif self.is_moving:
            self.led_indicator.setStyleSheet("background-color: green;")
        else:
            self.led_indicator.setStyleSheet("background-color: red;")

    def send_goal(self):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = 5.0
        goal_msg.pose.pose.position.y = -5.0
        goal_msg.pose.pose.orientation.w = 1.0
        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.goal_response_callback)
        self.is_moving = True

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f"Current robot position: {feedback.current_pose}")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected!")
            return

        self.get_logger().info("Goal accepted!")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result()
        if result.status == 4:  # SUCCEEDED
            self.get_logger().info("Goal reached!")
            self.is_moving = False

    def return_home(self):
        # Send a goal to return to the home position
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.pose.position.x = 0.0
        goal_msg.pose.pose.position.y = -5.0
        goal_msg.pose.pose.orientation.w = 1.0
        self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self.is_moving = True


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()

    rclpy_executor = rclpy.executors.SingleThreadedExecutor()
    rclpy_executor.add_node(video_player)

    try:
        while rclpy.ok():
            rclpy_executor.spin_once(timeout_sec=0.1)
            app.processEvents()
    finally:
        video_player.destroy_node()
        rclpy.shutdown()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
