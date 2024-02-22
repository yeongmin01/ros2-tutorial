import time
import rclpy

from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int32MultiArray
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy

class WinningChecker(Node):

    def __init__(self):
        super().__init__('winning_checker')
        self.random_number = []
        self.callback_group = ReentrantCallbackGroup()

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value

        QOS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)
        
        self.winning_checker_sunscriber = self.create_subscription(
            Int32MultiArray,
            'lotto_result',
            self.result_check,
            QOS_RKL10V,
            callback_group=self.callback_group)

    def result_check(self, msg):
        self.random_number = msg.data

        self.get_logger().info('random number : {}'.format(msg.data))

