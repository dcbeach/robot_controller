#!/usr/bin/env python3
import rclpy #python library for ROS2
from rclpy.node import Node
import smbus			#import SMBus module of I2C
from time import sleep   
from geometry_msgs.msg import Twist
from mpu6050 import mpu6050

class MyNode(Node):

    def __init__(self):
        super().__init__("imu_node")
        self.mpu = mpu6050(0x68)
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer_ = self.create_timer(0.5, self.send_imu_command)
        self.get_logger().info("IMU Node has started.")
    
    def send_imu_command(self):
        accel_data = self.mpu.get_accel_data()
        #Read Accelerometer raw value
        acc_x = accel_data['x']
        acc_y = accel_data['y']
        acc_z = accel_data['z']
        gyro_data = self.mpu.get_gyro_data()
        #Read Gyroscope raw value
        gyro_x = gyro_data['x']
        gyro_y = gyro_data['y']
        gyro_z = gyro_data['z']

        msg = Twist()
        msg.linear.x = acc_x
        msg.linear.y = acc_y
        msg.linear.z = acc_z
        msg.angular.x = gyro_x
        msg.angular.y = gyro_y
        msg.angular.z = gyro_z
        self.cmd_vel_pub_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    #CODE GOES HERE
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

#This lets us execute the file from terminal
if __name__== '__main__':
    main()