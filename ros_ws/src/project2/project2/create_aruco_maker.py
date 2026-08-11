"""Generate the nine board-cell ArUco textures used by the Gazebo world."""

from pathlib import Path

import cv2


def main():
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    output_directory = Path(__file__).resolve().parents[1] / 'models' / 'textures'
    output_directory.mkdir(parents=True, exist_ok=True)

    for marker_id in range(9):
        if hasattr(cv2.aruco, 'generateImageMarker'):
            marker = cv2.aruco.generateImageMarker(dictionary, marker_id, 200)
        else:
            marker = cv2.aruco.drawMarker(dictionary, marker_id, 200)
        output_path = output_directory / f'aruco_{marker_id}.png'
        if not cv2.imwrite(str(output_path), marker):
            raise RuntimeError(f'failed to write {output_path}')
        print(f'generated {output_path}')


if __name__ == '__main__':
    main()
