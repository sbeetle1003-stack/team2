import os
from glob import glob

from setuptools import find_packages, setup


package_name = 'project2'


def collect_data_files(directory):
    """Collect a directory tree for installation under share/project2."""
    data_files = []
    for root, directories, filenames in os.walk(directory):
        directories[:] = [name for name in directories if name != '__pycache__']
        files = [
            os.path.join(root, filename)
            for filename in filenames
            if not filename.endswith(('.pyc', '.pyo'))
        ]
        if files:
            destination = os.path.join('share', package_name, root)
            data_files.append((destination, files))
    return data_files


data_files = [
    (
        'share/ament_index/resource_index/packages',
        ['resource/' + package_name],
    ),
    ('share/' + package_name, ['package.xml']),
    (
        os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py'),
    ),
    (
        os.path.join('share', package_name, 'config'),
        glob('config/*.yaml'),
    ),
]
data_files.extend(collect_data_files('world'))
data_files.extend(collect_data_files('models'))


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='team2',
    maintainer_email='luckymijin0608@gmail.com',
    description='Vision-based tic-tac-toe simulation and pick-and-place controller.',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'aruco_tf_publisher = project2.aruco_tf_publisher:main',
            'multi_aruco_tf_sub = project2.multi_aruco_tf_sub:main',
            'pick_place_controller = project2.pick_place_controller:main',
            'tic_tac_toe_referee = project2.tic_tac_toe_referee:main',
            'tic_tac_toe_manual_test = project2.tic_tac_toe_manual_test:main',
        ],
    },
)
