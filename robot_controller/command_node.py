#!/usr/bin env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class CommandNode(Node):
    def __init__(self):
        super().__init__("cmd_node")
        self.cmd_vel_pub_ = self.create_publisher(String, "/robot/movement", 10)
        self.timer_ = self.create_timer(10, self.send_velocity_command)
        self.get_logger().info("Command Node Initiated...")

    def send_velocity_command(self):
        msg = String()
        msg.data = "Move:1:1"
        self.cmd_vel_pub_.publish(str(msg.data))
        

def main(args=None):
    rclpy.init(args=args)
    node = CommandNode()
    rclpy.spin(node)
    rclpy.shutdown()

#This lets us execute the file from terminal
if __name__== '__main__':
    main()