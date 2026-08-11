from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'project2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='boyfriend51',
    maintainer_email='luckymijin0608@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "tic_tac_toe_referee = project2.tic_tac_toe_referee:main",
            "tictactoe_twin_sync = project2.tictactoe_twin_sync:main",
            "create_aruco_maker = project2.create_aruco_maker:main",
            "digital_twin_robot = project2.digital_twin_robot:main",
            "digital_twin_board = project2.digital_twin_board:main",
            "board_detector = project2.board_detector:main",
           
            
        ],
    },
)
