from  include import yd_lidarX2

scan_data = yd_lidarX2.Ydlidar_ros_wrapper()

if __name__ == '__main__':
    scan_data.scan_data()
    