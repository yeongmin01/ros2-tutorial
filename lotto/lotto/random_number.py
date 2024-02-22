import random
import rclpy

from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from std_msgs.msg import Int32MultiArray

class RandomNumber(Node):

    def __init__(self):
        super().__init__('random_number')
        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value
        self.declare_parameter('min_random_num', 1)
        self.min_random_num = self.get_parameter('min_random_num').value
        self.declare_parameter('max_random_num', 45)
        self.max_random_num = self.get_parameter('max_random_num').value

        QOS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)

        self.lotto_result_publisher = self.create_publisher(
            Int32MultiArray,
            'lotto_result',
            QOS_RKL10V)

        self.timer = self.create_timer(1.0, self.publish_random_number)

    def publish_random_number(self):

        msg = Int32MultiArray()
        random_number_list = []
        for i in range(6):
            number = int(random.randint(self.min_random_num, self.max_random_num))

            while True:
                if (random_number_list!= [] and (number in random_number_list)):
                    number = int(random.randint(self.min_random_num, self.max_random_num))
                break

            random_number_list.append(number)

        random_number_list.sort()
        
        extra_number = int(random.randint(self.min_random_num, self.max_random_num))
        while True:
            if (extra_number in random_number_list):
                extra_number = int(random.randint(self.min_random_num, self.max_random_num))
            break

        random_number_list.append(extra_number)

        self.get_logger().info('random_number: {0}'.format(random_number_list))

        msg.data = random_number_list
        self.lotto_result_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    try:
        random_number = RandomNumber()
        try:
            rclpy.spin(random_number)
        except KeyboardInterrupt:
            random_number.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            random_number.destroy_node()
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()