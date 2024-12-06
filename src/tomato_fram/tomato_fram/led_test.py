from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5 import uic
import os

# Define the script directory and path to the .ui file
script_dir = os.path.dirname(os.path.realpath(__file__))
ui_file_path = os.path.join(script_dir, 'tomato.ui')

# Load the UI file using uic.loadUi
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file_path, self)  # Load your UI from the .ui file

        # Find the LED widget by its name in the .ui file
        self.led_indicator = self.findChild(QWidget, "led_indicator")
        
        # Find the button to trigger the LED color change
        self.total_request = self.findChild(QPushButton, "total_request")
        self.total_request.clicked.connect(self.toggle_led)  # Connect button click to toggle LED

    def toggle_led(self):
        # Example logic: Change LED color on button click
        if self.led_indicator.styleSheet() == "background-color: red; border-radius: 20px;":
            self.led_indicator.setStyleSheet("background-color: green; border-radius: 20px;")
        else:
            self.led_indicator.setStyleSheet("background-color: red; border-radius: 20px;")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
