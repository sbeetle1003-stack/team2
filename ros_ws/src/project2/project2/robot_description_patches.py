"""Gazebo-only additions to the stock OpenManipulator-X robot_description.

open_manipulator_description does not ship a wrist camera, so this module
adds one programmatically wherever the URDF gets processed (the launch
file's Gazebo model and pick_place_controller's MoveIt planning model),
instead of forking the shared external package.
"""

import xml.etree.ElementTree as ET

CAMERA_LINK_NAME = 'camera_link'
CAMERA_MOUNT_JOINT_NAME = 'camera_mount_joint'
CAMERA_PARENT_LINK = 'link5'
# Above and behind link5's origin, tilted steeply down so the camera looks
# past the gripper toward the board/pieces it is reaching for. Mounting it
# lower (closer to link5.stl's own z=0.04 top surface) instead pointed the
# camera into the gripper's own underside. Visually sits slightly off the
# body; functional board visibility was prioritized over a flush mount.
CAMERA_MOUNT_XYZ = '-0.04 0 0.12'
CAMERA_MOUNT_RPY = '0 0.9 0'


def add_wrist_camera(robot_root, *, include_sensor):
    """Add camera_link, fixed-mount it to link5, and optionally its sensor.

    Mutates robot_root (an xml.etree URDF root) in place. Safe to call on
    both the Gazebo spawn model (include_sensor=True) and MoveIt's planning
    model (include_sensor=False, which has no use for a Gazebo sensor tag).
    """
    camera_link = ET.SubElement(robot_root, 'link', {'name': CAMERA_LINK_NAME})

    inertial = ET.SubElement(camera_link, 'inertial')
    ET.SubElement(inertial, 'mass', {'value': '0.02'})
    ET.SubElement(
        inertial,
        'inertia',
        {
            'ixx': '0.000005', 'ixy': '0', 'ixz': '0',
            'iyy': '0.000005', 'iyz': '0',
            'izz': '0.000005',
        },
    )

    for tag in ('visual', 'collision'):
        element = ET.SubElement(camera_link, tag)
        geometry = ET.SubElement(element, 'geometry')
        ET.SubElement(geometry, 'box', {'size': '0.02 0.03 0.02'})
        if tag == 'visual':
            material = ET.SubElement(element, 'material', {'name': 'camera_housing'})
            ET.SubElement(material, 'color', {'rgba': '0.1 0.1 0.1 1'})

    joint = ET.SubElement(
        robot_root,
        'joint',
        {'name': CAMERA_MOUNT_JOINT_NAME, 'type': 'fixed'},
    )
    ET.SubElement(joint, 'parent', {'link': CAMERA_PARENT_LINK})
    ET.SubElement(joint, 'child', {'link': CAMERA_LINK_NAME})
    ET.SubElement(
        joint,
        'origin',
        {'xyz': CAMERA_MOUNT_XYZ, 'rpy': CAMERA_MOUNT_RPY},
    )

    if not include_sensor:
        return

    gazebo = ET.SubElement(robot_root, 'gazebo', {'reference': CAMERA_LINK_NAME})
    sensor = ET.SubElement(
        gazebo, 'sensor', {'name': 'gripper_camera', 'type': 'camera'},
    )
    ET.SubElement(sensor, 'always_on').text = 'true'
    ET.SubElement(sensor, 'visualize').text = 'true'
    ET.SubElement(sensor, 'update_rate').text = '15'
    ET.SubElement(sensor, 'topic').text = '/gripper_camera/image_raw'
    camera = ET.SubElement(sensor, 'camera')
    ET.SubElement(camera, 'horizontal_fov').text = '1.1'
    image = ET.SubElement(camera, 'image')
    ET.SubElement(image, 'width').text = '640'
    ET.SubElement(image, 'height').text = '480'
    clip = ET.SubElement(camera, 'clip')
    ET.SubElement(clip, 'near').text = '0.02'
    ET.SubElement(clip, 'far').text = '3.0'
