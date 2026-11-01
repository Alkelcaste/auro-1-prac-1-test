import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String
from nav_msgs.msg import Odometry


class OdomPosPublisher(Node):
    def __init__(self):
        super().__init__('odom_pos_publisher')

        self.subscription = self.create_subscription(
            Odometry,
            'odom',
            self.odometry_callback,
            10)

        self.subscription  # prevent unused variable warning

    def odometry_callback(self, msg):
        self.get_logger().info(f'Position: {msg.pose.pose.position}\n')

def main(args=None):
    try:
        with rclpy.init(args=args):
            odom_pos_publisher = OdomPosPublisher()

            rclpy.spin(odom_pos_publisher)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()