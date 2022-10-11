#!/usr/bin/env python3
import rclpy #python library for ROS2
from rclpy.node import Node
import serial
import time
from example_interfaces.msg import String

print("Attempting to initiate serial")
try:
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=11500, timeout=0.1)
except Exception:
    print(Exception)

class MyNode(Node):

    def __init__(self):
        super().__init__("serial_node")
        #self.send_command_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.get_logger().info("Serial has started.")
        self.subscription = self.create_subscription(
            String,
            '/robot/movement',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info:('I heard: "%s"' % msg.data)
        self.send_command(msg)
    
    def send_command(self, msg):
        self.write(msg.data)
        response = self.read()
        if (msg.data == response):
            self.get_logger().info("Arduino confirmed command...")
        else:
            self.get_logger().info("Arduino command failed...")    
        #self.cmd_vel_pub_.publish(command)

    def read():
        data = arduino.readline()
        return data

    def write(self, x):
        arduino.write(bytes(x, 'ut-8f'))
        time.sleep(0.05)

def main(args=None):
    rclpy.init(args=args)

    #CODE GOES HERE
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

#This lets us execute the file from terminal
if __name__== '__main__':
    main()