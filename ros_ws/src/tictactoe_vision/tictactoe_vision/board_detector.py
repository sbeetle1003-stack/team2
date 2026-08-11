import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8MultiArray


# BoardState
EMPTY = 0
HUMAN = 1   # BLUE
ROBOT = 2   # RED
UNKNOWN = 3

STATE_NAMES = {
    EMPTY: "EMPTY",
    HUMAN: "HUMAN",
    ROBOT: "ROBOT",
    UNKNOWN: "UNKNOWN",
}

# Perspective 보정 영상에서 실제 게임판만 잘라내기 위한 비율.
# 현재 인쇄물에서는 0.12부터 시작하고 필요하면 조정하면 된다.
BOARD_CROP_MARGIN_RATIO = 0.12

# 최종 게임판 크기: 600 x 600 → 각 Cell은 200 x 200
BOARD_SIZE = 600

# Cell 가장자리의 검은 격자선을 색상 판정에서 제외하기 위한 여백 비율
CELL_INNER_MARGIN_RATIO = 0.12

# ROI 안에서 이 비율 이상 색상이 검출되면 말이 있다고 판단
COLOR_RATIO_THRESHOLD = 0.08


BOARD_MARKER_IDS = {
    0: "top_left",
    1: "top_right",
    2: "bottom_right",
    3: "bottom_left",
}

WARP_SIZE = 800


def get_marker_centers(corners, ids):
    """검출된 ArUco marker 중 ID 0~3의 중심 좌표를 반환한다."""
    marker_centers = {}

    if ids is None:
        return marker_centers

    ids_flat = ids.flatten()

    for marker_corners, marker_id in zip(corners, ids_flat):
        if marker_id not in BOARD_MARKER_IDS:
            continue

        # marker_corners shape: (1, 4, 2)
        points = marker_corners[0]

        # 네 꼭짓점의 평균값 = marker 중심
        center = points.mean(axis=0)

        marker_centers[int(marker_id)] = center

    return marker_centers


def warp_board(frame, marker_centers):
    """
    ArUco ID 0,1,2,3의 중심점을 기준으로
    카메라 영상을 정면의 정사각형 영상으로 원근 보정한다.

    ID 배치:
        0 = Top-Left
        1 = Top-Right
        2 = Bottom-Right
        3 = Bottom-Left
    """
    required_ids = {0, 1, 2, 3}

    # 4개의 marker가 모두 검출되지 않았으면 보정하지 않는다.
    if not required_ids.issubset(marker_centers.keys()):
        return None

    src_pts = np.array(
        [
            marker_centers[0],  # TL
            marker_centers[1],  # TR
            marker_centers[2],  # BR
            marker_centers[3],  # BL
        ],
        dtype=np.float32,
    )

    dst_pts = np.array(
        [
            [0, 0],
            [WARP_SIZE - 1, 0],
            [WARP_SIZE - 1, WARP_SIZE - 1],
            [0, WARP_SIZE - 1],
        ],
        dtype=np.float32,
    )

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

    warped = cv2.warpPerspective(
        frame,
        matrix,
        (WARP_SIZE, WARP_SIZE),
    )

    return warped



def crop_game_board(warped):
    """
    ArUco 4개 중심을 기준으로 보정된 영상에서
    실제 3x3 게임판 영역만 중앙 crop한 뒤 600x600으로 정규화한다.

    현재는 인쇄물의 마커-게임판 배치가 고정되어 있으므로
    고정 비율 crop을 사용한다.
    """
    height, width = warped.shape[:2]

    margin_x = int(width * BOARD_CROP_MARGIN_RATIO)
    margin_y = int(height * BOARD_CROP_MARGIN_RATIO)

    board = warped[
        margin_y : height - margin_y,
        margin_x : width - margin_x,
    ]

    board = cv2.resize(
        board,
        (BOARD_SIZE, BOARD_SIZE),
        interpolation=cv2.INTER_LINEAR,
    )

    return board


def split_board_rois(board_img):
    """
    600x600 게임판을 3x3 ROI로 분할한다.

    반환:
        [(cell_index, roi, (x1, y1, x2, y2)), ...]
    """
    cell_size = BOARD_SIZE // 3
    rois = []

    for row in range(3):
        for col in range(3):
            cell_index = row * 3 + col

            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            roi = board_img[y1:y2, x1:x2]

            rois.append(
                (
                    cell_index,
                    roi,
                    (x1, y1, x2, y2),
                )
            )

    return rois


def classify_cell(roi):
    """
    Cell ROI의 HSV 색상 비율을 이용해 상태를 판정한다.

    BLUE → HUMAN
    RED  → ROBOT
    색상 없음 → EMPTY
    BLUE와 RED가 동시에 강하게 검출 → UNKNOWN
    """
    height, width = roi.shape[:2]

    # 검은 격자선과 Cell 경계를 판정에서 제외
    margin_x = int(width * CELL_INNER_MARGIN_RATIO)
    margin_y = int(height * CELL_INNER_MARGIN_RATIO)

    inner_roi = roi[
        margin_y : height - margin_y,
        margin_x : width - margin_x,
    ]

    hsv = cv2.cvtColor(inner_roi, cv2.COLOR_BGR2HSV)

    # BLUE
    blue_lower = np.array([90, 80, 50], dtype=np.uint8)
    blue_upper = np.array([135, 255, 255], dtype=np.uint8)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

    # RED는 HSV Hue 범위가 양 끝으로 나뉘므로 두 mask를 합친다.
    red_lower_1 = np.array([0, 80, 50], dtype=np.uint8)
    red_upper_1 = np.array([10, 255, 255], dtype=np.uint8)

    red_lower_2 = np.array([170, 80, 50], dtype=np.uint8)
    red_upper_2 = np.array([179, 255, 255], dtype=np.uint8)

    red_mask_1 = cv2.inRange(hsv, red_lower_1, red_upper_1)
    red_mask_2 = cv2.inRange(hsv, red_lower_2, red_upper_2)
    red_mask = cv2.bitwise_or(red_mask_1, red_mask_2)

    total_pixels = inner_roi.shape[0] * inner_roi.shape[1]

    blue_ratio = cv2.countNonZero(blue_mask) / total_pixels
    red_ratio = cv2.countNonZero(red_mask) / total_pixels

    blue_detected = blue_ratio >= COLOR_RATIO_THRESHOLD
    red_detected = red_ratio >= COLOR_RATIO_THRESHOLD

    if blue_detected and red_detected:
        state = UNKNOWN
    elif blue_detected:
        state = HUMAN
    elif red_detected:
        state = ROBOT
    else:
        state = EMPTY

    return state, blue_ratio, red_ratio


def analyze_board(board_img):
    """
    9개 Cell을 판정하고 BoardState와 표시용 영상을 반환한다.

    BoardState:
        0 = EMPTY
        1 = HUMAN
        2 = ROBOT
        3 = UNKNOWN
    """
    display = board_img.copy()
    board_state = [EMPTY] * 9

    rois = split_board_rois(board_img)

    for cell_index, roi, (x1, y1, x2, y2) in rois:
        state, blue_ratio, red_ratio = classify_cell(roi)
        board_state[cell_index] = state

        # Cell 경계 표시
        cv2.rectangle(
            display,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

        # Cell 번호 + 판정 상태
        label = f"{cell_index}: {STATE_NAMES[state]}"
        cv2.putText(
            display,
            label,
            (x1 + 8, y1 + 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 0),
            2,
        )

        # 디버깅용 색상 비율
        ratio_text = f"B:{blue_ratio:.2f} R:{red_ratio:.2f}"
        cv2.putText(
            display,
            ratio_text,
            (x1 + 8, y1 + 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (0, 0, 0),
            1,
        )

    return board_state, display


class BoardDetectorNode(Node):
    """카메라 영상을 분석하여 틱택토 BoardState를 ROS2 topic으로 publish한다."""

    def __init__(self):
        super().__init__("board_detector")

        # /board_state:
        # 0 = EMPTY, 1 = HUMAN(BLUE), 2 = ROBOT(RED), 3 = UNKNOWN
        self.board_state_pub = self.create_publisher(
            Int8MultiArray,
            "/board_state",
            10,
        )

        # 카메라 설정
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("카메라를 열 수 없습니다.")

        # OpenCV 4.6.0용 ArUco 설정
        self.aruco_dict = cv2.aruco.Dictionary_get(
            cv2.aruco.DICT_4X4_50
        )
        self.parameters = cv2.aruco.DetectorParameters_create()

        # 같은 상태를 계속 publish하지 않도록 이전 상태 저장
        self.previous_board_state = None

        # 약 10 Hz로 카메라 처리
        self.timer = self.create_timer(
            0.1,
            self.timer_callback,
        )

        self.get_logger().info(
            "Board detector started. Publishing: /board_state"
        )

    def timer_callback(self):
        # 1. 카메라 frame 획득
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warning(
                "카메라 프레임을 읽을 수 없습니다."
            )
            return

        # 원본 frame은 Perspective Transform용으로 보존
        display_frame = frame.copy()

        # 2. ArUco 검출
        corners, ids, rejected = cv2.aruco.detectMarkers(
            frame,
            self.aruco_dict,
            parameters=self.parameters,
        )

        # 3. ID 0~3 marker 중심점 계산
        marker_centers = get_marker_centers(corners, ids)

        # 4. 검출 결과 표시
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(
                display_frame,
                corners,
                ids,
            )

            for marker_id, center in marker_centers.items():
                cx, cy = center.astype(int)

                cv2.circle(
                    display_frame,
                    (cx, cy),
                    5,
                    (0, 0, 255),
                    -1,
                )

                cv2.putText(
                    display_frame,
                    f"C{marker_id}",
                    (cx + 8, cy - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2,
                )

        # 5. ArUco 4개가 모두 보이면 Perspective Transform
        warped = warp_board(frame, marker_centers)

        if warped is not None:
            # 6. 실제 3x3 게임판 추출
            board_img = crop_game_board(warped)

            # 7. ROI 분할 + 색상 판정
            board_state, board_display = analyze_board(board_img)

            # 8. 상태가 달라졌을 때만 ROS2 publish
            if board_state != self.previous_board_state:
                msg = Int8MultiArray()
                msg.data = board_state

                self.board_state_pub.publish(msg)

                self.get_logger().info(
                    f"BoardState: {board_state}"
                )

                self.previous_board_state = board_state.copy()

            cv2.imshow(
                "Perspective Board",
                warped,
            )

            cv2.imshow(
                "Board State",
                board_display,
            )

        # 9. 원본 검출 화면
        cv2.imshow(
            "Tic-Tac-Toe Board Detector",
            display_frame,
        )

        # OpenCV GUI event 처리
        # q/ESC는 창 자체를 닫기 위한 보조 기능.
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            self.get_logger().info(
                "q/ESC pressed. Stop the node with Ctrl+C."
            )

    def destroy_node(self):
        """노드 종료 시 카메라와 OpenCV 창을 정리한다."""
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()

        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = None

    try:
        node = BoardDetectorNode()
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    except RuntimeError as error:
        print(error)

    finally:
        if node is not None:
            node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
