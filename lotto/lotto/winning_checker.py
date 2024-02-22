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
        self.winning_number = []
        self.number_math = 0
        self.extra_number = False
        self.result = ''
        self.total_result = [0,0,0,0,0,0] # 1, 2, 3, 4, 5, 꽝

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
            self.winning_result,
            QOS_RKL10V)

    def winning_result(self, msg):
        self.random_number = msg.data

        self.number_match_check()
        self.result_check()

        self.get_logger().info('random number : {0} \n'.format(self.random_number))
        self.get_logger().info('winning number : {0} \n'.format(self.winning_number))
        self.get_logger().info('result : {0} \n'.format(self.result))
        self.get_logger().info('total result : {0} \n'.format(self.total_result)) # 1, 2, 3, 4, 5, 꽝

    def number_match_check(self):
        self.number_math = 0
        self.extra_number = False

        for i in range(6):
            if self.random_number[i] in self.winning_number:
                self.number_math += 1
        
        if (self.random_number[6] == self.winning_number[6]):
            self.extra_number = True

    def result_check(self):
        if (self.extra_number) :
            match self.number_math:
                case 0:
                    self.result = '0개의 번호가 맞았습니다.'
                    self.total_result[5] += 1
                case 1:
                    self.result = '1개의 번호가 맞았습니다.'
                    self.total_result[5] += 1
                case 2:
                    self.result = '2개의 번호가 맞았습니다.'
                    self.total_result[4] += 1
                case 3:
                    self.result = '3개의 번호가 맞았습니다.'
                    self.total_result[3] += 1
                case 4:
                    self.result = '4개의 번호가 맞았습니다.'
                    self.total_result[2] += 1
                case 5:
                    self.result = '5개의 번호가 맞았습니다.'
                    self.total_result[1] += 1
                case 6:
                    self.result = '6개의 번호가 맞았습니다.'
                    self.total_result[0] += 1
        else : 
            match self.number_math:
                case 0:
                    self.result = '0개의 번호가 맞았습니다.'
                    self.total_result[5] += 1
                case 1:
                    self.result = '1개의 번호가 맞았습니다.'
                    self.total_result[5] += 1
                case 2:
                    self.result = '2개의 번호가 맞았습니다.'
                    self.total_result[5] += 1
                case 3:
                    self.result = '3개의 번호가 맞았습니다.'
                    self.total_result[4] += 1
                case 4:
                    self.result = '4개의 번호가 맞았습니다.'
                    self.total_result[3] += 1
                case 5:
                    self.result = '5개의 번호가 맞았습니다.'
                    self.total_result[2] += 1
                case 6:
                    self.result = '6개의 번호가 맞았습니다.'
                    self.total_result[0] += 1    

def main(args=None):
    rclpy.init(args=args)
    try:
        lotto = WinningChecker()
        for i in range(7):
            number = int(input("Write {}'s number : ".format(i)))
            lotto.winning_number.append(number)
        try:
            rclpy.spin(lotto)
        except KeyboardInterrupt:
            lotto.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            lotto.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()