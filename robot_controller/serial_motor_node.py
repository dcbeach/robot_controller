#!/usr/bin/env python3
import rclpy #python library for ROS2
from rclpy.node import Node
import serial
import time
from std_msgs.msg import String

print("Attempting to initiate serial")
try:
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=0.1)
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

    def listener_callback(self, msg: String):
        self.get_logger().info(str(msg.data))
        self.send_command(str(msg.data))
    
    def send_command(self, msg):
        print("The message to write = " + msg)
        self.write(msg)
        response = ""
        while response == "":
            response = self.read()

        if (response == "CR"):
            self.get_logger().info("Arduino confirmed command...")
        else:
            self.get_logger().info(response)  
            self.get_logger().info("No Response")  
        #self.cmd_vel_pub_.publish(command)

    def read(self):
        data = arduino.readline().decode('utf-8')
        print(data)
        return data

    def write(self, x):
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.1)

def main(args=None):
    rclpy.init(args=args)

    #CODE GOES HERE
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

#This lets us execute the file from terminal
if __name__== '__main__':
    main()