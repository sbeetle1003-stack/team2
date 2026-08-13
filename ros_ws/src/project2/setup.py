import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'project2'

def collect_data_files(directory):
    """Collect a directory tree for installation under share/project2."""
    data_files = []
    if not os.path.exists(directory):
        return data_files
        
    for root, directories, filenames in os.walk(directory):
        # __pycache__ 및 숨김 파일/폴더 제외
        directories[:] = [name for name in directories if name != '__pycache__' and not name.startswith('.')]
        files = [
            os.path.join(root, filename)
            for filename in filenames
            if not filename.endswith(('.pyc', '.pyo'))
        ]
        if files:
            # install/share/project2 경로 아래에 원본 디렉토리 구조 그대로 복사
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

# world 폴더 안의 .sdf 및 관련 파일 자동 수집
data_files.extend(collect_data_files('world'))

# models 폴더 안의 모든 하위 디렉토리(o_mark.sdf, x_mark.sdf, textures 등) 전체 자동 수집
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
            'digital_twin_board = project2.digital_twin_board:main',
            'digital_twin_robot = project2.digital_twin_robot:main',
            'create_aruco_maker = project2.create_aruco_maker:main',
            'manipulation_geometry = project2.manipulation_geometry:main',
            'spawn_test_node = project2.spawn_test_node:main',
        ],
    },
)





# import os
# from glob import glob

# from setuptools import find_packages, setup


# package_name = 'project2'


# def collect_data_files(directory):
#     """Collect a directory tree for installation under share/project2."""
#     data_files = []
#     for root, directories, filenames in os.walk(directory):
#         directories[:] = [name for name in directories if name != '__pycache__']
#         files = [
#             os.path.join(root, filename)
#             for filename in filenames
#             if not filename.endswith(('.pyc', '.pyo'))
#         ]
#         if files:
#             destination = os.path.join('share', package_name, root)
#             data_files.append((destination, files))
#     return data_files


# data_files = [
#     (
#         'share/ament_index/resource_index/packages',
#         ['resource/' + package_name],
#     ),
#     ('share/' + package_name, ['package.xml']),
#     (
#         os.path.join('share', package_name, 'launch'),
#         glob('launch/*.launch.py'),
#     ),
#     (
#         os.path.join('share', package_name, 'config'),
#         glob('config/*.yaml'),
#     ),
#     # (
#     #     os.path.join('share', package_name, 'models', 'textures'), 
#     #     glob('models/textures/*')
#     # ),
# ]
# data_files.extend(collect_data_files('world'))
# data_files.extend(collect_data_files('models'))


# setup(
#     name=package_name,
#     version='0.1.0',
#     packages=find_packages(exclude=['test']),
#     data_files=data_files,
#     install_requires=['setuptools'],
#     zip_safe=True,
#     maintainer='team2',
#     maintainer_email='luckymijin0608@gmail.com',
#     description='Vision-based tic-tac-toe simulation and pick-and-place controller.',
#     license='Apache-2.0',
#     extras_require={'test': ['pytest']},
#     entry_points={
#         'console_scripts': [
#             'aruco_tf_publisher = project2.aruco_tf_publisher:main',
#             'multi_aruco_tf_sub = project2.multi_aruco_tf_sub:main',
#             'pick_place_controller = project2.pick_place_controller:main',
#             'tic_tac_toe_referee = project2.tic_tac_toe_referee:main',
#             'tic_tac_toe_manual_test = project2.tic_tac_toe_manual_test:main',
#             'digital_twin_board = project2.digital_twin_board:main',
#             'digital_twin_robot = project2.digital_twin_robot:main',
#             'create_aruco_maker = project2.create_aruco_maker:main',
#             'manipulation_geometry = project2.manipulation_geometry:main',
#             'spawn_test_node = project2.spawn_test_node:main',
            
            
#         ],
#     },
# )
