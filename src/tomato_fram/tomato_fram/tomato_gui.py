import sys
import os
import rclpy
import numpy as np
from sensor_msgs.msg import Image
from rclpy.node import Node
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic
import cv2

# Get the UI file path automatically
script_dir = os.path.dirname(os.path.realpath(__file__))
ui_file_path = os.path.join(script_dir, 'tomato.ui')

form_class = uic.loadUiType(ui_file_path)[0]

class VideoPlayer(QMainWindow, form_class, Node):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setupUi(self)
        Node.__init__(self, 'video_player_node')

        # ROS 2 Image Subscription
        self.image_subscription = self.create_subscription(
            Image,  # Message type
            '/tomato/image',  # Topic name
            self.image_sub_callback,  # Callback function
            10  # Queue size
        )

        # Set up the timer for updating the frame in the GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms (~33 FPS)

        self.label_video = self.findChild(QLabel, "label_image")
        # Find the LED widget by its name in the .ui file
        self.led_indicator = self.findChild(QWidget, "led_indicator")

        # Find the button to trigger the LED color change
        self.start_button = self.findChild(QPushButton, "start_button")
        self.start_button.clicked.connect(self.toggle_led)  # Connect button click to toggle LED
        self.start_button.clicked.connect(self.TextBox_exc_clicked)

        self.latest_frame = None  # To store the latest frame from the camera


    def image_sub_callback(self, msg):
        """ROS callback for image topic."""
        # Convert ROS image message to numpy array
        image_data = np.frombuffer(msg.data, np.uint8)
        frame = np.reshape(image_data, (msg.height, msg.width, 3))

        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            self.latest_frame = qt_image  # Store the frame

    def update_frame(self):
        """Update the GUI with the latest frame."""
        if self.latest_frame is not None:
            self.label_video.setPixmap(QPixmap.fromImage(self.latest_frame))

    def TextBox_exc_clicked(self):
        self.show_total.setText('Hello world!')

    def toggle_led(self):
        # Example logic: Change LED color on button click
        if self.led_indicator.styleSheet() == "background-color: red; border-radius: 20px;":
            self.led_indicator.setStyleSheet("background-color: green; border-radius: 20px;")
        else:
            self.led_indicator.setStyleSheet("background-color: red; border-radius: 20px;")
    def closeEvent(self, event):
        """Properly shut down ROS 2 node."""
        rclpy.shutdown()
        event.accept()

def main():
    # Initialize ROS 2 node
    rclpy.init()

    # Create an instance of the VideoPlayer (which is also a ROS 2 node)
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()

    # Spin the ROS 2 node and handle PyQt events in the main thread
    while rclpy.ok():
        rclpy.spin_once(player, timeout_sec=0.1)  # Spin ROS with a small timeout
        app.processEvents()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
