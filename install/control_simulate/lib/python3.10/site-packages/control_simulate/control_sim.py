# import sys
# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import Twist
# from PyQt5 import QtWidgets, QtCore
# from .ui.speed_coltrol import Ui_MainWindow  # 引入生成的UI文件
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import QTimer
# import cv2

# class TeleopTwistKeyboard(Node):
#     def __init__(self):
#         super().__init__('teleop_twist_keyboard_gui')
#         self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
       
#         # PyQt5 初始化
#         self.app = QtWidgets.QApplication(sys.argv)
#         self.init_ui()

#     def init_ui(self):
#         MainWindow = QtWidgets.QMainWindow()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(MainWindow)
        
        
#         # 連接按鈕到對應的回調函數
#         self.ui.pushButton_4.clicked.connect(self.forward)
#         self.ui.pushButton_2.clicked.connect(self.backward)
#         self.ui.pushButton.clicked.connect(self.turn_left)
#         self.ui.pushButton_3.clicked.connect(self.turn_right)
#         self.ui.pushButton_5.clicked.connect(self.stop)
        
#         MainWindow.show()
#         self.app.exec_()
    

#     def forward(self):
#         twist = Twist()
#         twist.linear.x = 1.0
#         self.publisher_.publish(twist)

#     def backward(self):
#         twist = Twist()
#         twist.linear.x = -1.0
#         self.publisher_.publish(twist)

#     def turn_left(self):
#         twist = Twist()
#         twist.angular.z = 1.0
#         self.publisher_.publish(twist)

#     def turn_right(self):
#         twist = Twist()
#         twist.angular.z = -1.0
#         self.publisher_.publish(twist)
    
#     def stop(self):
#         twist = Twist()
#         self.publisher_.publish(twist)

# def main(args=None):
#     rclpy.init(args=args)
#     teleop_twist_keyboard = TeleopTwistKeyboard()
#     teleop_twist_keyboard.get_logger().info('Node started')
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
'''
只有視訊框
'''
# from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer
# import sys
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2

# class ImageSubscriber(Node):
#     def __init__(self, video_label):
#         super().__init__('image_subscriber')
#         self.video_label = video_label  # QLabel for displaying the image
#         self.bridge = CvBridge()  # Used to convert ROS Image message to OpenCV image
#         self.subscription = self.create_subscription(
#             Image,
#             '/image',
#             self.listener_callback,
#             10)
#         self.subscription  # to prevent unused variable warning

#     def listener_callback(self, msg):
#         # Convert ROS Image message to OpenCV image
#         cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
#         cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
#         qt_image = self.convert_cv_to_pixmap(cv_image)
#         self.video_label.setPixmap(qt_image)

#     def convert_cv_to_pixmap(self, cv_img):
#         """Convert an OpenCV image to QPixmap"""
#         rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#         p = convert_to_Qt_format.scaled(self.video_label.width(), self.video_label.height(), 
#                                         QtCore.Qt.KeepAspectRatio)
#         return QPixmap.fromImage(p)

# def main(args=None):
#     rclpy.init(args=args)
#     app = QtWidgets.QApplication(sys.argv)

#     # Assume `Form` is your main window and `videoLabel` is already created.
#     Form = QtWidgets.QWidget()
#     Form.setWindowTitle('ROS2 Image Viewer')
#     Form.resize(640, 480)
    
#     # Assuming `videoLabel` is the QLabel you have created
#     videoLabel = QtWidgets.QLabel(Form)
#     videoLabel.setObjectName("videoLabel")
#     videoLabel.setGeometry(10, 10, 620, 460)

#     # Create ROS2 node
#     image_subscriber = ImageSubscriber(videoLabel)

#     # Start the GUI
#     Form.show()

#     # Setup the QTimer to periodically call ROS2 spin
#     timer = QTimer()
#     timer.timeout.connect(lambda: rclpy.spin_once(image_subscriber, timeout_sec=0.1))
#     timer.start(10)  # 10 ms for a high refresh rate

#     # Run the PyQt5 application
#     exit_code = app.exec_()
    
#     # Clean up ROS2 node
#     image_subscriber.destroy_node()
#     rclpy.shutdown()

#     sys.exit(exit_code)

# if __name__ == '__main__':
#     main()


import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGridLayout
import cv2
import threading

# 假設你的 speed_coltrol 模塊和 Ui_MainWindow 類被放在當前目錄下的 ui 模塊中
from .ui.speed_coltrol import Ui_MainWindow  # 根據你的檔案結構修改這裡的導入路徑

class TeleopTwistKeyboard(Node):
    def __init__(self, ui):
        super().__init__('teleop_twist_keyboard_gui')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10)
        self.cv_bridge = CvBridge()
        self.current_frame = None
        self.ui = ui

    def image_callback(self, msg):
        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")
            self.current_frame = cv_image
        except CvBridgeError as e:
            self.get_logger().error('Could not convert image: %s' % e)

    def publish_twist(self, linear, angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.publisher_.publish(twist)

# 以下代碼應該放在 PyQt5 的主窗口類中
class MainWindow(QMainWindow):
    def __init__(self, node):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.node = node

        # 設置主視窗的佈局
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QGridLayout(self.central_widget)
        
        # 將由 Qt Designer 生成的 UI 小部件添加到佈局中
        layout.addWidget(self.ui.videoLabel, 0, 0, 1, 3)  # videoLabel 占用第一行，跨越三列
        layout.addWidget(self.ui.pushButton_4, 1, 1)  # 前進按鈕放在第一行，第一列
        layout.addWidget(self.ui.pushButton_2, 4, 1)  # 後退按鈕放在第四行，第一列
        layout.addWidget(self.ui.pushButton, 2, 0)    # 左轉按鈕放在第二行，第零列
        layout.addWidget(self.ui.pushButton_3, 2, 2)  # 右轉按鈕放在第二行，第二列
        layout.addWidget(self.ui.pushButton_5, 2, 1, 1, 1)  # 停止按鈕放在第二行，第二列，跨越一列

        # 設置小部件的大小策略
        self.ui.videoLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # 連接按鈕到對應的回調函數
        self.ui.pushButton_4.clicked.connect(lambda: self.node.publish_twist(1.0, 0.0))  # 前進
        self.ui.pushButton_2.clicked.connect(lambda: self.node.publish_twist(-1.0, 0.0))  # 後退
        self.ui.pushButton.clicked.connect(lambda: self.node.publish_twist(0.0, 1.0))  # 左轉
        self.ui.pushButton_3.clicked.connect(lambda: self.node.publish_twist(0.0, -1.0))  # 右轉
        self.ui.pushButton_5.clicked.connect(lambda: self.node.publish_twist(0.0, 0.0))  # 停止

        # 初始化視訊更新的定時器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video_frame)
        self.timer.start(30)  # 每30毫秒更新一次視訊

    def update_video_frame(self):
        frame = self.node.current_frame
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.ui.videoLabel.setPixmap(pixmap.scaled(self.ui.videoLabel.width(), self.ui.videoLabel.height(), QtCore.Qt.KeepAspectRatio))

def main(args=None):
    rclpy.init(args=args)
    teleop_node = TeleopTwistKeyboard(None)
    rclpy.spin_once(teleop_node, timeout_sec=0.1)  # 快速初始化回調

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(teleop_node)
    teleop_node.ui = main_window.ui  # 將 UI 關聯到 ROS2 節點
    main_window.show()

    # 使用多線程運行 ROS2 節點
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(teleop_node)

    def run_executor():
        executor.spin()

    # 在單獨的線程中運行 ROS2 節點
    thread = threading.Thread(target=run_executor)
    thread.start()

    exit_code = app.exec_()
    executor.shutdown()
    teleop_node.destroy_node()
    rclpy.shutdown()
    thread.join()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
