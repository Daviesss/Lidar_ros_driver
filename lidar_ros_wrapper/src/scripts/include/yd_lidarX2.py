#!/usr/bin/env python3
'''
  Node implementation of YDLidar X2 ros wrapper,
  contains library , class ,methods 
  and also implementation of the ROS 1 wrappper for YDlidarX2
'''
# import Libraries..
import rospy
import ydlidar 
from sensor_msgs.msg import LaserScan


# implementation class....
class Ydlidar_ros_wrapper:
    def __init__(self):
        rospy.init_node('lidar_ros_wrapper',anonymous=True)
        self.laser_scan_data = LaserScan() # store laser scan data type 
        self.laser_pub = rospy.Publisher("/scan",LaserScan,queue_size=10) # Publish over to a topic name called "/scan"
        self.port = rospy.get_param('~port',"/dev/ttyUSB0")
        self.buad_rate = rospy.get_param('~baudrate',115200)
        self.scan_frequency = rospy.get_param('~scan_frequency',10.0)
        self.sample_rate = rospy.get_param('~sampleRate',9)
        self.singlechannel = rospy.get_param('~SingleChannel',True) # Set to True for pub laser scan.....
        self.max_range = rospy.get_param('~max_range',12.0)
        # self.min_range = rospy.get_param('~min_range',6.0)
        self.lidar_type = rospy.get_param('~lidar_type', ydlidar.TYPE_TRIANGLE)
        self.device_type = rospy.get_param('~device_type',ydlidar.YDLIDAR_TYPE_SERIAL)  
        
        
        ############################################################################
        self.YDLIDAR = ydlidar.CYdLidar() # Initialize the Lidar
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropSerialPort,self.port) # initiliaze the port...
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropSerialBaudrate,self.buad_rate) 
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropScanFrequency,self.scan_frequency)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropReversion,self.sample_rate)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropSingleChannel,self.singlechannel)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropMinAngle,self.max_range)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropLidarType,self.lidar_type)
        self.YDLIDAR.setlidaropt(ydlidar.LidarPropDeviceType,self.device_type)
        
        rate = rospy.Rate(10)  # 10 Hz

        
     
    # get laser scan data , process it and publish it over to ros...  
    def scan_data(self,msg):
      while not rospy.is_shutdown():
        # Read Lidar Scan data
        self.laser_scan_data = ydlidar.LaserScan() # get data from the laser scanner...
        self.scan = LaserScan()
        # Populate the scan data....
        data_ = self.YDLIDAR.doProcessSimple(self.laser_scan_data)
        if data_ :  # if true
          angle_range = []
          ran = []
          laser_intensity = []
          
          for points in self.laser_scan_data:
            angle_range.append(points.angle)
            
            
         
          
          
          
          # Publish "/scan" topic over to ros....
          # self.laser_pub.publish(self.scan)
          
          
          
          
          
          
        
      
      
        
        
        
        
        
        
        
        
        
        