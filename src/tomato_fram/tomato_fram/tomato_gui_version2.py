import sys
import cv2
import rclpy
from std_msgs.msg import String
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class RobotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Robot Controller')

        self.video_label = QLabel(self)
        self.start_button = QPushButton('Start', self)
        self.return_button = QPushButton('Return', self)
        self.led_indicator = QLabel(self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.return_button)
        self.layout.addWidget(self.led_indicator)

        self.setLayout(self.layout)

        # ROS 2 setup
        rclpy.init()
        self.node = rclpy.create_node('robot_gui')
        self.status_pub = self.node.create_publisher(String, 'robot_status', 10)

        # OpenCV setup for robot camera feed
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video_feed)
        self.timer.start(30)

        self.start_button.clicked.connect(self.start_robot)
        self.return_button.clicked.connect(self.return_home)

    def update_video_feed(self):
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to QImage and update the label
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(q_image))

    def start_robot(self):
        # Send start command to robot (ROS 2 logic)
        self.status_pub.publish(String(data="start"))
        # Update LED indicator to green for movement
        self.led_indicator.setStyleSheet("background-color: green")

    def return_home(self):
        # Send return command to robot (ROS 2 logic)
        self.status_pub.publish(String(data="return_home"))
        # Update LED indicator to red for stop
        self.led_indicator.setStyleSheet("background-color: red")

    def update_led_indicator(self, status):
        if status == "moving":
            self.led_indicator.setStyleSheet("background-color: green")
        elif status == "stopped":
            self.led_indicator.setStyleSheet("background-color: red")
        elif status == "harvesting":
            self.led_indicator.setStyleSheet("background-color: yellow")

def main():
    app = QApplication(sys.argv)
    window = RobotGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
