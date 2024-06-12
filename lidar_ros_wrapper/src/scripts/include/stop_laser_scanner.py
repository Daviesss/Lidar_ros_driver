import rospy 
import ydlidar
from std_srvs.srv import Empty,EmptyResponse


# implementation class....
class stop_laser_scanner_data:
    def __init__(self):
        self.stop_laser_scanner = rospy.Service("/stop_lidar",Empty,self.stop_lidar) # service to stop laser scanner
        self.laser = ydlidar.CYdLidar()
      
        
    # rosservice to stop the lidar(laser scanner)...
    def stop_lidar(self,request):
        # rospy.loginfo("The lidar sensor has stopped.....")
        self.laser.turnOff()
        rospy.loginfo("Laser scan has stopped.......")
        return EmptyResponse()

        
