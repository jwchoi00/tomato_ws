import os
import sys
import threading
import math
import time  # Import the time module
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from tomato_interfaces.msg import TomatoDetected
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5 import uic
from cv_bridge import CvBridge
import numpy as np
import cv2
from geometry_msgs.msg import PoseWithCovarianceStamped

# UI file path
script_dir = os.path.dirname(os.path.realpath(__file__))
ui_file_path = os.path.join(script_dir, 'tomato.ui')
form_class = uic.loadUiType(ui_file_path)[0]

class VideoPlayer(QMainWindow, form_class, Node):
    update_image_signal = pyqtSignal(QImage)
    update_led_signal = pyqtSignal(str)

    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setupUi(self)
        Node.__init__(self, 'video_player')

        
        # Subscriptions and action client
        self.image_subscription = self.create_subscription(
            Image, '/tomato/image', self.image_callback, 10
        )
        self.detect_subscribe = self.create_subscription(
            TomatoDetected, '/tomato/detected', self.tomato_detected_state_callback, 10
        )
        self.action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, 10
        )
        # Timer for GUI updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(30)

        # Variables for state tracking
        self.latest_frame = None
        self.bridge = CvBridge()
        self.is_moving = False
        self.tomato_detected = False
        
        # Define waypoints
        self.current_position = {'x': 0.0, 'y': 0.0}
        self.waypoints = [
            {'x': 0.0, 'y': 0.0},  # Home position
            {'x': -1.0, 'y': -1.0},  # Waypoint 1
            {'x': -1.5, 'y': -1.0},  # Waypoint 2
            {'x': -2.0, 'y': -1.0},  # Waypoint 3
            {'x': -2.5, 'y': -1.0},  # Waypoint 4
        ]
        self.current_waypoint_index = 0  # Start from the first waypoint

        # UI components
        self.led_indicator = self.findChild(QWidget, "led_indicator")
        self.start_button = self.findChild(QPushButton, "start_button")
        self.start_button.clicked.connect(self.send_goal)
        self.return_button = self.findChild(QPushButton, "return_button")
        self.return_button.clicked.connect(self.return_home)

        # QLabel to display the image
        self.image_label = self.findChild(QLabel, "label_image")  # Ensure this QLabel exists in your UI

        # Start image processing in a separate thread
        self.image_thread = threading.Thread(target=self.image_processing_loop, daemon=True)
        self.image_thread.start()

        # Start navigation control in a separate thread
        self.navigation_thread = threading.Thread(target=self.navigation_loop, daemon=True)
        self.navigation_thread.start()

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, 3)
            hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)

            # Detect red color (tomato)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            mask = cv2.inRange(hsv_image, lower_red, upper_red)

            # Set detection flag if any red pixels are found
            if np.sum(mask) > 0:
                self.tomato_detected = True
            else:
                self.tomato_detected = False

            # Convert image for PyQt display
            qt_image = QImage(cv_image.data, msg.width, msg.height, QImage.Format_RGB888)
            self.latest_frame = qt_image
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def tomato_detected_state_callback(self, msg):
        self.tomato_detected = msg.detected
        print(f'tomato_detected : {self.tomato_detected}')

    def pose_callback(self, msg):
        # Update current robot position from AMCL or localization data
        self.current_position['x'] = msg.pose.pose.position.x
        self.current_position['y'] = msg.pose.pose.position.y

    def set_led_color(self, color):
        # Set LED color based on the input color
        if color == 'green':
            self.led_indicator.setStyleSheet('background-color: green')
        elif color == 'yellow':
            self.led_indicator.setStyleSheet('background-color: yellow')
        elif color == 'red':
            self.led_indicator.setStyleSheet('background-color: red')

    def update_gui(self):
        if self.is_moving:
            self.set_led_color('green')  # LED turns green when moving
        elif self.is_harvesting:
            self.set_led_color('yellow')  # LED turns yellow when harvesting
        else:
            self.set_led_color('red')  # LED turns red when stopped

        # Call other functions...
        self.check_tomato_and_stop(self.current_position)

    def send_goal(self):
        if self.current_waypoint_index < len(self.waypoints):
            # Get the current waypoint
            waypoint = self.waypoints[self.current_waypoint_index]
            goal_msg = NavigateToPose.Goal()
            goal_msg.pose.header.frame_id = "map"
            goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
            goal_msg.pose.pose.position.x = waypoint['x']
            goal_msg.pose.pose.position.y = waypoint['y']
            goal_msg.pose.pose.orientation.w = 3.14

            # Send the goal to the robot
            self.action_client.wait_for_server()
            future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
            future.add_done_callback(self.goal_response_callback)

            self.is_moving = True
    # def send_goal(self):
    #     goal_msg = NavigateToPose.Goal()
    #     goal_msg.pose.header.frame_id = "map"
    #     goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
    #     goal_msg.pose.pose.position.x = -2.75
    #     goal_msg.pose.pose.position.y = -1.25
    #     goal_msg.pose.pose.orientation.w = 1.0

    #     self.action_client.wait_for_server()
    #     future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
    #     future.add_done_callback(self.goal_response_callback)

    #     self.is_moving = True

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        #self.get_logger().info(f"Current robot position: {feedback.current_pose}")

    def goal_response_callback(self, future):
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().info("Goal rejected!")
                return
            self.get_logger().info("Goal accepted!")
            self.current_goal_handle = goal_handle
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.result_callback)
    # def goal_response_callback(self, future):
    #     goal_handle = future.result()
    #     if not goal_handle.accepted:
    #         self.get_logger().info("Goal rejected!")
    #         return
    #     self.get_logger().info("Goal accepted!")
    #     self.current_goal_handle = goal_handle
    #     result_future = goal_handle.get_result_async()
    #     result_future.add_done_callback(self.result_callback)

    # def result_callback(self, future):
    #     result = future.result()
    #     if result.status == 4:  # SUCCEEDED
    #         self.get_logger().info("Goal reached!")
    #         self.is_moving = False
    # def result_callback(self, future):
    #     result = future.result()
    #     if result.status == 4:  # SUCCEEDED
    #         self.get_logger().info("Goal reached!")
    #         self.is_moving = False

    #         # Move to the next waypoint
    #         self.current_waypoint_index += 1
    #         if self.current_waypoint_index < len(self.waypoints):
    #             self.send_goal()

    def result_callback(self, future):
        result = future.result()
        if result.status == 4:  # SUCCEEDED
            self.get_logger().info("Goal reached!")
            self.is_moving = False

            # Move to the next waypoint if necessary
            self.current_waypoint_index += 1
            if self.current_waypoint_index < len(self.waypoints):
                self.send_goal()
            else:
                self.get_logger().info("All waypoints completed!")

    def return_home(self):
        # Send a goal to return to the home position
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = 0.0
        goal_msg.pose.pose.position.y = 0.0
        goal_msg.pose.pose.orientation.w = 3.14

        self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self.is_moving = True

    def check_tomato_and_stop(self, current_position):
        # Ensure the current waypoint index is within the bounds of the waypoints list
        if self.current_waypoint_index >= len(self.waypoints):
            self.get_logger().info("All waypoints completed!")
            return  # Exit if no more waypoints exist
        # Get the current waypoint
        waypoint = self.waypoints[self.current_waypoint_index]
        # Calculate the distance between the current position and the waypoint
        distance = math.sqrt((current_position['x'] - waypoint['x'])**2 + (current_position['y'] - waypoint['y'])**2)
        # Check if the robot has reached the waypoint (within a tolerance of 0.1 meters)
        if distance < 0.1 and self.is_moving:
            self.get_logger().info(f"Reached waypoint {self.current_waypoint_index + 1}!")
            self.is_moving = False
            # Stop the robot (optional, depending on your requirements)
            if hasattr(self, 'current_goal_handle'):
                self.current_goal_handle.cancel_goal_async()
            # Pause for 3 seconds
            QTimer.singleShot(3000, self.resume_navigation)
    # def check_tomato_and_stop(self):
    #     if self.tomato_detected and self.is_moving:
    #         self.get_logger().info("Tomato detected! Stopping the robot.")
    #         # Cancel the goal using the stored goal handle
    #         if hasattr(self, 'current_goal_handle'):
    #             self.current_goal_handle.cancel_goal_async()
    #         self.is_moving = False
    #         # Resume navigation after 3 seconds
    #         QTimer.singleShot(3000, self.resume_navigation)

    def resume_navigation(self):
        self.get_logger().info("Resuming navigation.")

        # Move to the next waypoint
        self.current_waypoint_index += 1
        if self.current_waypoint_index < len(self.waypoints):
            self.send_goal()
        else:
            self.get_logger().info("All waypoints completed!")


    def image_processing_loop(self):
        # This loop runs in a separate thread to process the images continuously
        rclpy.spin(self)

    def navigation_loop(self):
        # This loop runs in a separate thread to handle navigation tasks
        while rclpy.ok():
            time.sleep(1)  # Simulate some time for robot navigation tasks

    def update_image_display(self, qt_image):
        # Convert the QImage to QPixmap and set it in the QLabel
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    
    # Connect signal to update QLabel with the new image
    video_player.update_image_signal.connect(video_player.update_image_display)

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

if __name__ == '__main__':
    main()
