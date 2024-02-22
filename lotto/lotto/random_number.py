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
        self.declare_parameter('min_random_num', 0)
        self.min_random_num = self.get_parameter('min_random_num').value
        self.declare_parameter('max_random_num', 45)
        self.max_random_num = self.get_parameter('max_random_num').value
        self.add_on_set_parameters_callback(self.update_parameter)

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
        
        for i in range(7):
            msg.data.append = int(random.randint(self.min_random_num, self.max_random_num))

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