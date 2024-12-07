import os
import sys
import rclpy
import numpy as np
import logging
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import Image
from nav2_msgs.action import NavigateToPose
from tomato_interfaces.msg import TomatoDetected
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from cv_bridge import CvBridge
import math
from geometry_msgs.msg import Quaternion

# UI file path
script_dir = os.path.dirname(os.path.realpath(__file__))
ui_file_path = os.path.join(script_dir, 'tomato.ui')
form_class = uic.loadUiType(ui_file_path)[0]

class QTextEditLogHandler(logging.Handler):
    def __init__(self, text_edit_widget):
        super().__init__()
        self.text_edit = text_edit_widget

    def emit(self, record):
        log_message = self.format(record)
        # Ensure the message is added to the QTextEdit widget in the main thread
        QTimer.singleShot(0, lambda: self.text_edit.append(log_message))


class VideoPlayer(QMainWindow, form_class, Node):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        Node.__init__(self, 'video_player')

        # Initialize UI
        self.setupUi(self)
        self.led_indicator = self.findChild(QWidget, "led_indicator")  # QWidget for LED status
        self.start_button = self.findChild(QPushButton, "start_button")
        self.start_button.clicked.connect(self.send_goal)
        self.return_button = self.findChild(QPushButton, "return_button")
        self.return_button.clicked.connect(self.return_home)

        # QTextEdit widget for logging
        self.show_total = self.findChild(QTextEdit, "show_total")

        # Set up custom logging handler
        self.logger = logging.getLogger('rclpy')
        self.logger.setLevel(logging.INFO)
        self.log_handler = QTextEditLogHandler(self.show_total)
        formatter = logging.Formatter('%(message)s')
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

        # ROS 2 Subscriptions and action client
        self.detect_subscriber = self.create_subscription(
            TomatoDetected, '/tomato/detected', self.tomato_detected_callback, 50
        )
        self.image_subscriber = self.create_subscription(
            Image, '/tomato/image', self.image_callback, 50
        )
        self.action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')

        # State variables
        self.is_moving = False
        self.is_harvesting = False
        self.tomato_detected = False
        self.current_waypoint_index = 0
        self.bridge = CvBridge()
        self.latest_frame = None
        self.retry_count = 0  # Initialize retry_count

        # Define waypoints
        self.waypoints = [
            {'x': -1.0, 'y': -1.0},  # Waypoint 1
            {'x': -1.5, 'y': -1.0},  # Waypoint 2
            {'x': -2.0, 'y': -1.0},  # Waypoint 3
            {'x': -2.5, 'y': -1.0},  # Waypoint 4
        ]

        # Timer for UI updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(30)
        self.logger.info("Logging initialized successfully.")

    def tomato_detected_callback(self, msg):
        self.tomato_detected = msg.detected
        if self.tomato_detected == True:
            self.logger.info(f"Tomato detected: {self.tomato_detected}")

    def image_callback(self, msg):
        try:
            # Convert ROS Image to QImage
            cv_image = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, 3)
            qt_image = QImage(cv_image.data, msg.width, msg.height, QImage.Format_RGB888)
            self.latest_frame = qt_image  # Assign the latest frame to the attribute
        except Exception as e:
            self.logger.error(f"Error displaying image: {e}")

    def set_led_color(self, color):
        if color == 'green':
            self.led_indicator.setStyleSheet('background-color: green')
        elif color == 'yellow':
            self.led_indicator.setStyleSheet('background-color: yellow')
        elif color == 'red':
            self.led_indicator.setStyleSheet('background-color: red')

    def update_gui(self):
        if self.latest_frame is not None:
            self.findChild(QLabel, "label_image").setPixmap(QPixmap.fromImage(self.latest_frame))
        if self.is_moving:
            self.set_led_color('green')  # Green: Moving
        elif self.is_harvesting:
            self.set_led_color('yellow')  # Yellow: Harvesting
        else:
            self.set_led_color('red')  # Red: Stopped

    def create_quaternion_from_yaw(self, yaw):
        """Convert yaw angle (in radians) to quaternion."""
        q = Quaternion()
        q.w = math.cos(yaw / 2)
        q.z = math.sin(yaw / 2)
        q.x = 0.0
        q.y = 0.0
        return q
    
    def send_goal(self):
        if self.current_waypoint_index < len(self.waypoints):
            target_yaw = -135.0  # Target yaw angle in radians (facing East)
            quaternion = self.create_quaternion_from_yaw(target_yaw)
            waypoint = self.waypoints[self.current_waypoint_index]
            goal_msg = NavigateToPose.Goal()
            goal_msg.pose.header.frame_id = "map"
            goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
            goal_msg.pose.pose.position.x = waypoint['x']
            goal_msg.pose.pose.position.y = waypoint['y']
            goal_msg.pose.pose.orientation = quaternion

            self.logger.info(f"Sending goal: {goal_msg.pose.pose.position.x}, {goal_msg.pose.pose.position.y}")
            self.action_client.wait_for_server()
            future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
            future.add_done_callback(self.goal_response_callback)
            self.is_moving = True

    def feedback_callback(self, feedback_msg):
        # Handle feedback (if needed)
        pass

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if goal_handle is None:
            self.logger.error("Goal handle is None!")
            return
        if not goal_handle.accepted:
            self.logger.info("Goal rejected!")
            return

        self.logger.info("Goal accepted!")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result()
        if result.status == 4:  # SUCCEEDED
            self.logger.info(f"Waypoint {self.current_waypoint_index + 1} reached!")
            self.is_moving = False
            self.logger.info('Moving stopped')
            if self.tomato_detected:
                self.logger.info('Going to harvesting mode')
                self.is_harvesting = True
                QTimer.singleShot(3000, self.resume_navigation)  # Wait 3 seconds
            else:
                self.current_waypoint_index -= 1
                QTimer.singleShot(1000, self.retry_search_tree)

    def retry_search_tree(self):
        # Retry the search at the same waypoint if no tomatoes were detected
        if not self.tomato_detected:
            self.retry_count += 1
            self.logger.info(f"Tomato not detected at waypoint {self.current_waypoint_index + 1}. Retry {self.retry_count}...")
            if self.retry_count < 3:  # Retry up to 3 times
                self.send_goal()  # Resend the goal to the same waypoint
            else:
                self.logger.info(f"Max retries reached at waypoint {self.current_waypoint_index + 1}. Moving to next waypoint.")
                self.retry_count = 0  # Reset retry counter
                self.resume_navigation()
        else:
            self.logger.info("Tomato found, proceeding with harvest.")
            self.is_harvesting = True
            QTimer.singleShot(3000, self.resume_navigation)

    def resume_navigation(self):
        self.is_harvesting = False
        self.logger.info("Resuming navigation.")
        self.current_waypoint_index += 1
        if self.current_waypoint_index < len(self.waypoints):
            self.send_goal()
        else:
            self.logger.info("All waypoints completed!")

    def return_home(self):
        target_yaw = -135.0  # Target yaw angle in radians (facing East)
        quaternion = self.create_quaternion_from_yaw(target_yaw)
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = 0.0
        goal_msg.pose.pose.position.y = 0.0
        goal_msg.pose.pose.orientation = quaternion
        self.logger.info(f"Sending goal: {goal_msg.pose.pose.position.x}, {goal_msg.pose.pose.position.y}")

        if not self._context.ok():
            self.logger.error("ROS context is invalid!")
            return

        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.home_goal_response_callback)
        self.is_moving = True

    def home_goal_response_callback(self, future):
        goal_handle = future.result()
        if goal_handle is None:
            self.logger.error("Goal handle is None!")
            return
        if not goal_handle.accepted:
            self.logger.info("Goal rejected!")
            return

        self.logger.info("Goal accepted!")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.home_result_callback)

    def home_result_callback(self, future):
        result = future.result()
        if result.status == 4:  # SUCCEEDED
            self.logger.info("Home position reached!")
            self.is_moving = False
            self.current_waypoint_index = 0
        else:
            self.logger.error("Failed to reach home position!")

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    rclpy_executor = rclpy.executors.SingleThreadedExecutor()
    rclpy_executor.add_node(player)

    try:
        while rclpy.ok():
            rclpy_executor.spin_once(timeout_sec=0.1)
            app.processEvents()
    finally:
        player.destroy_node()
        rclpy.shutdown()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
