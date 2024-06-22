from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os

def generate_launch_description():
    #獲取機器人模型路徑
    robot_model_path = os.path.expanduser('src/wanderbot_integrate/wanderbot4W_description')
    robot_model_file = os.path.join(robot_model_path, 'launch', 'wanderbot.launch.py')

    #底盤路徑
    ros2_stm32_bridge_path = os.path.expanduser('src/wanderbot_integrate/ros2_stm32_bridge')
    ros2_stm32_bridge_file = os.path.join(ros2_stm32_bridge_path, 'launch', 'driver.launch.py')

    #激光雷達驅動包路徑
    laser_path = os.path.expanduser("src/wanderbot_integrate/LSLIDAR_X_ROS2/lslidar_driver")
    laser_file = os.path.join(laser_path, "launch", "lsn10_launch.py")
    
    #---------------------------------

    #wanderbot模型啟動
    wanderbot_action = IncludeLaunchDescription(PythonLaunchDescriptionSource([
        robot_model_file]))
    
    #底盤啟動
    ros2_stm32_bridge = IncludeLaunchDescription(PythonLaunchDescriptionSource([
        ros2_stm32_bridge_file
    ]))

    #相機啟動
    camera_action = Node(
        package= "usb_cam",
        executable= "usb_cam_node_exe",
        arguments= ["--ros-args", "--params-file", "src/wanderbot_integrate/camera_config/usb_cam.yaml"]
    )

    #激光雷達啟動
    laser_action = IncludeLaunchDescription(PythonLaunchDescriptionSource([
        laser_file
    ]))


    return LaunchDescription([
        wanderbot_action,
        camera_action,
        laser_action,
        ros2_stm32_bridge,
    ])