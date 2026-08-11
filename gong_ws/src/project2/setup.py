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
            "aruco_tf_publisher = project2.aruco_tf_publisher:main",
            "tic_tac_toe_referee = project2.tic_tac_toe_referee:main",
            "tic_tac_toe_manual_test = project2.tic_tac_toe_manual_test:main",
            "multi_aruco_tf_sub = project2.multi_aruco_tf_sub:main",
        ],
    },
)
