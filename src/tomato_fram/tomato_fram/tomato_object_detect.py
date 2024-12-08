import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from tomato_interfaces.msg import TomatoDetected
from cv_bridge import CvBridge
import numpy as np
import cv2
from time import time
# Define HSV range for detecting red (tomato color)
LOWER_RED1 = np.array([0, 100, 100])
UPPER_RED1 = np.array([10, 255, 255])
LOWER_RED2 = np.array([160, 100, 100])
UPPER_RED2 = np.array([179, 255, 255])

class TomatoDetectionNode(Node):
    def __init__(self):
        super().__init__('tomato_detector')
        self.subscription = self.create_subscription(
            Image, '/tb1/camera/image_raw', self.image_callback, 10
        )
        self.publisher = self.create_publisher(Image, '/tomato/image', 10)
        self.detect_publisher = self.create_publisher(TomatoDetected, '/tomato/detected', 10)
        self.bridge = CvBridge()
        self.last_log_time = 0  # 마지막 로그 시간을 기록할 변수
        self.log_interval = 1.0  # 로그를 찍는 간격(초)
        self.detected = False

    def image_callback(self, msg):
        try:
            # ROS 이미지를 OpenCV 이미지로 변환
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.process_image(cv_image)
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def process_image(self, image):
        try:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Detect red areas
            mask1 = cv2.inRange(hsv_image, LOWER_RED1, UPPER_RED1)
            mask2 = cv2.inRange(hsv_image, LOWER_RED2, UPPER_RED2)
            red_mask = cv2.bitwise_or(mask1, mask2)

            contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            self.detected = False

            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.detected = True

            current_time = time()
            if self.detected and (current_time - self.last_log_time > self.log_interval):
                self.get_logger().info("토마토 발견!")
                self.last_log_time = current_time
            else:
                self.detected = False

            ros_image = self.bridge.cv2_to_imgmsg(image, "bgr8")
            self.publisher.publish(ros_image)
            detected_msg = TomatoDetected()
            detected_msg.detected = self.detected
            self.detect_publisher.publish(detected_msg)
        except Exception as e:
            self.get_logger().error(f"Image processing error: {e}")
        
def main(args=None):
    rclpy.init(args=args)
    node = TomatoDetectionNode()  # 노드 생성
    try:
        rclpy.spin(node)  # 노드 실행
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()  # 노드 종료
        rclpy.shutdown()  # ROS 종료

if __name__ == "__main__":
    main()
