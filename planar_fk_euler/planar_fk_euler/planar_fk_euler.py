import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState


class JointStatesSubscriber(Node):
    def __init__(self):
        super().__init__('joint_states_subscriber')

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_states_callback,
            10)

        self.subscription  # prevent unused variable warning

    def joint_states_callback(self, msg):
        self.get_logger().info(f'Joint States: {msg.position}\n')

def main() -> None:
    rclpy.init()
    node = JointStatesSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    print('Hi from planar_fk_euler.')


if __name__ == '__main__':
    main()
