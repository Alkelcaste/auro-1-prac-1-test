import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState


class PlanarFKEuler(Node):
    def __init__(self):
        super().__init__('planar_fk_euler')

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10)

        self.pose_publisher = self.create_publisher(PoseStamped, 'ee_pose_stamped', 10)

    def joint_state_callback(self, msg: JointState):
        # Extract joint angles
        q1 = msg.position[0]
        q2 = msg.position[1]

        # Compute forward kinematics
        L1 = 0.4  # Length of the first link
        L2 = 0.3  # Length of the second link

        x = L1 * rclpy.math.cos(q1) + L2 * rclpy.math.cos(q1 + q2)
        y = L1 * rclpy.math.sin(q1) + L2 * rclpy.math.sin(q1 + q2)
        phi = q1 + q2  # Yaw angle

        # Create PoseStamped message
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'base_link'
        pose_msg.pose.position.x = x
        pose_msg.pose.position.y = y
        pose_msg.pose.position.z = 0.0
        pose_msg.pose.orientation.z = phi  # Store yaw in orientation.z for simplicity

        # Publish the end-effector pose
        self.pose_publisher.publish(pose_msg)

def main() -> None:
    try:
        with rclpy.init():
            planar_fk_euler = PlanarFKEuler()
            rclpy.spin(planar_fk_euler)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    


if __name__ == '__main__':
    main()
