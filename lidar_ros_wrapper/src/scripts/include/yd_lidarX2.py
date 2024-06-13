#!/usr/bin/env python3
"""
  Node implementation of YDLidar X2 ROS wrapper,
  contains library, class, methods
  and also implementation of the ROS 1 wrapper for YDLidarX2.

  Author: Davies Iyanuoluwa Ogunsina 
  Email: Davisogunsina@gmail.com
  Linkedlin: https://www.linkedin.com/in/davies-iyanuoluwa-ogunsina/
  
  MIT License

  Copyright (c) [2024] Davies Iyanuoluwa Ogunsina

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
"""
import rospy
import ydlidar
from sensor_msgs.msg import LaserScan
import math, random
# import rosservice library
from std_srvs.srv import Empty,EmptyResponse

# Implementation class
class Ydlidar_ros_wrapper:
    def __init__(self):
        rospy.init_node('lidar_ros_wrapper', anonymous=True)
        self.laser_pub = rospy.Publisher("/Scan_data", LaserScan, queue_size=10)  # Publish to the topic named "/Scan_data"
        self.stop_laser_scanner = rospy.Service("/stop_lidar",Empty,self.stop_lidar) # service to stop laser scanner
        self.port = rospy.get_param('~port', "/dev/ttyUSB0")
        self.baud_rate = rospy.get_param('~baudrate', 115200)
        self.scan_frequency = rospy.get_param('~scan_frequency', 10.0)
        self.sample_rate = rospy.get_param('~sampleRate', 9)
        self.singlechannel = rospy.get_param('~SingleChannel', True)  # Set to True for pub laser scan
        self.max_range = rospy.get_param('~max_range', 12.0)
        self.lidar_type = rospy.get_param('~lidar_type', ydlidar.TYPE_TRIANGLE)
        self.device_type = rospy.get_param('~device_type', ydlidar.YDLIDAR_TYPE_SERIAL)
        
        

        self.YDLIDAR = ydlidar.CYdLidar()  # Initialize the Lidar
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropSerialPort, self.port)  # initialize the port
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropSerialBaudrate, self.baud_rate)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropScanFrequency, self.scan_frequency)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropReversion, self.sample_rate)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropSingleChannel, self.singlechannel)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropMaxRange, self.max_range)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropLidarType, self.lidar_type)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropDeviceType, self.device_type)

        self.rate = rospy.Rate(10)  # 10 Hz
    
    
    # rosservice to stop the lidar(laser scanner)...
    def stop_lidar(self,request):
        self.stop_key  = "k"
        self.start_key = "l"
        if input("Enter the main password to stop the lidar..") == self.stop_key:
            rospy.logwarn("Password to stop laser scanner correct, laser scanner stopping now.....")
            self.YDLIDAR.turnOff()
            if input("Enter the main password to start the lidar..") == self.start_key:
                rospy.logwarn("Password to stop laser scanner correct, laser scanner stopping now.....")
                self.YDLIDAR.turnOn()
        
        else:  
            rospy.logwarn("The laser scanner is still running....")    
            self.YDLIDAR.turnOn()
        # rospy.loginfo("Laser scan has stopped.......")
        return EmptyResponse()



    # initilize the lidar....
    def initialize_lidar(self):
        lidar = {'min_angle': -math.pi,
                 'max_angle': math.pi, 
                 'angle_increment': math.pi / 180.0, 
                 'min_range': 0.1, 
                 'max_range':12.0,
                 'scan_frequency': 10.0,}
        return lidar
    
    
    
    # Get the data of ranges, intensities and angles.
    def get_lidar_data(self):
        # Placeholder for LiDAR data retrieval
        num_measurements = 360  # My laser rotates in an angle of 360 degrees...
        ranges = [random.uniform(0.1, 16.0) for _ in range(num_measurements)]
        intensities = [random.uniform(0, 255) for _ in range(num_measurements)]
        angles = [self.lidar['min_angle'] + i * self.lidar['angle_increment'] for i in range(num_measurements)]
        return ranges, intensities, angles
 
 
 
    # Get laser scan data, process it and publish it to ROS(Method that has the main implementation....)
    def scan_data(self):   
        ret_ = self.YDLIDAR.initialize()
        if ret_ :
            self.YDLIDAR.turnOn()
            rospy.logerr("start Lidar scanning!")
        else:
            rospy.logerr("Failed to start Lidar scanning!")
        
        
        
        # Get the lidar parameter initilization stored in a varaible.....
        self.lidar = self.initialize_lidar()
        
        
        # Loop true.....  
        while not rospy.is_shutdown():
            ranges, intensities, angles = self.get_lidar_data()
            laser_scan_data = ydlidar.LaserScan()  # get data from the laser scanner
            if self.YDLIDAR.doProcessSimple(laser_scan_data):
                scan = LaserScan()
                scan.header.stamp = rospy.Time.now()
                scan.header.frame_id = "laser_frame"
                scan.angle_min = self.lidar['min_angle']
                scan.angle_max = self.lidar['max_angle']
                scan.angle_increment = self.lidar['angle_increment']
                # scan.time_increment = laser_scan_data.config.time_increment
                scan.scan_time = scan.scan_time / len(ranges)
                scan.range_min = self.lidar['min_range']
                scan.range_max = self.lidar['max_range']
                scan.ranges = ranges
                scan.intensities = intensities

                # Publish "/Scan_data" topic to ROS
                self.laser_pub.publish(scan)
            self.rate.sleep()
            
