#!/usr/bin env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from pynput import keyboard  # using module keyboard

class CommandNode(Node):
    def __init__(self):
        super().__init__("cmd_node")
        self.cmd_vel_pub_ = self.create_publisher(String, "/robot/movement", 10)
        self.get_logger().info("Keyboard Node Initiated...")
        self.wait_for_keypress();

    def wait_for_keypress(self):
        msg = String()
        msg.data = ""
        # Collect events until released
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()
        
        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

    def on_press(self, key):
        msg = String()
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
            msg.data = "Move:100/"
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
        self.send_velocity_command(msg)

    def on_release(self, key):
        msg = String()
        print('{0} released'.format(
            key))
        msg.data = "Stop:/"
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        self.send_velocity_command(msg)



        
        

    def send_velocity_command(self, msg: String):
        self.cmd_vel_pub_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    node = CommandNode()
    rclpy.spin(node)
    rclpy.shutdown()

#This lets us execute the file from terminal
if __name__== '__main__':
    main()