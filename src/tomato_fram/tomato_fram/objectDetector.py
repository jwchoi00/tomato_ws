import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
from time import time

# 붉은색의 HSV 범위 정의
lower_red1 = np.array([0, 100, 100])   # 낮은 범위의 빨간색
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100]) # 높은 범위의 빨간색
upper_red2 = np.array([179, 255, 255])

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # 구독할 토픽 이름
            self.image_callback,
            10)  # 큐 크기
        #처리된 이미지 전송
        self.publisher = self.create_publisher(
            Image,
            '/tomato/image',
            10
        )

        self.bridge = CvBridge()
        self.last_log_time = 0  # 마지막 로그 시간을 기록할 변수
        self.log_interval = 1.0  # 로그를 찍는 간격(초)
        self.tomato_detected = False  # Flag to indicate tomato detection

    def image_callback(self, msg):
        try:
            # ROS 이미지를 OpenCV 이미지로 변환
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.process_image(cv_image)
        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def process_image(self, image):
        # BGR 이미지를 HSV로 변환
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 붉은색 검출
        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # 붉은 영역 찾기
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # 특정 크기 이상의 객체만 감지
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                detected = True

        
        # 1초마다 로그 출력
        current_time = time()
        if detected and (current_time - self.last_log_time > self.log_interval):
            self.get_logger().info("토마토 발견!")
            self.last_log_time = current_time
        else:
            self.tomato_detected = False

        self.publish_processed_image(image)
        # 결과 출력
        # cv2.imshow("Tomato Detection", image)
        # cv2.waitKey(1)

    def publish_processed_image(self, image):
        try:
            # Convert the processed OpenCV image back to ROS message
            ros_image = self.bridge.cv2_to_imgmsg(image, "bgr8")
            self.publisher.publish(ros_image)
        except Exception as e:
            self.get_logger().error(f"Error publishing image: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetector()  # 노드 생성
    try:
        rclpy.spin(node)  # 노드 실행
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()  # 노드 종료
        rclpy.shutdown()  # ROS 종료

if __name__ == "__main__":
    main()
