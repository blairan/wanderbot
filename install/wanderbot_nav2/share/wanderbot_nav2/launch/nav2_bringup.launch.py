import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    #設置use_sim_time參數
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    #設置map存放路徑
    map_path = LaunchConfiguration(
        "map",
        default=os.path.join("/home/sunrise/wanderbot/src/maps", "my_room.yaml"))
    #nav2的參數文件路徑
    nav2_params_filename = "nav2_params.yaml"
    #nav2功能包路徑
    nav2_params_path = LaunchConfiguration(
        "params",
        default=os.path.join(get_package_share_directory("wanderbot_nav2"), "params", nav2_params_filename))
    #導航包nav2_bringup路徑
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=map_path,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value=nav2_params_path,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_params_path}.items(),
        )
    ])