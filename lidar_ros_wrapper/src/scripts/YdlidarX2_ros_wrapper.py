from  include import yd_lidarX2

pub_scan_data = yd_lidarX2.Ydlidar_ros_wrapper()

if __name__ == '__main__':
    pub_scan_data.scan_data()
    