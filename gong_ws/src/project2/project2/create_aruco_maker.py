import cv2
import cv2.aruco as aruco

# 사용할 ArUco 사전(Dictionary) 종류 선택 (예: 4x4 마커)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 0번부터 8번까지 총 9개의 마커 이미지 생성 (3x3 보드용)
for i in range(9):
    # generateImageMarker(dict, id, size_in_pixels)
    marker_image = aruco.generateImageMarker(dictionary, i, 200)
    
    # 파일로 저장 (예: workspace 경로 혹은 모델 폴더 내부에 저장)
    cv2.imwrite(f'aruco_marker_{i}.png', marker_image)

print("ArUco 마커 이미지 0~8번 생성 완료!")


# #!/usr/bin/env python3
# import cv2

# def main():
#     # 1. ArUco 사전 정의 (DICT_4X4_50)
#     aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

#     # 2. 생성할 마커 ID 설정 (로봇 6~10번, 사람 11~15번 등)
#     marker_ids = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#     marker_size = 200  # 마커 이미지 픽셀 크기

#     for m_id in marker_ids:
#         # 최신 및 호환성 문제가 없는 OpenCV 마커 생성 함수 사용
#         marker_img = cv2.aruco.generateImageMarker(aruco_dict, m_id, marker_size)
        
#         # 이미지 파일로 저장
#         filename = f"aruco_{m_id}.png"
#         cv2.imwrite(filename, marker_img)
#         print(f"ArUco 마커 ID {m_id} 생성 완료: {filename}")

# if __name__ == '__main__':
#     main()
    
    
    
'''
import cv2

print(cv2.__version__)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

marker_id = 6
marker_size = 1000

marker = cv2.aruco.drawMarker(
    dictionary,
    marker_id,
    marker_size,
)

marker_with_margin = cv2.copyMakeBorder(
    marker,
    100,
    100,
    100,
    100,
    cv2.BORDER_CONSTANT,
    value=255,
)

output_path = "aruco_6.png"

success = cv2.imwrite(output_path, marker_with_margin)

if not success:
    raise RuntimeError(f"이미지 저장 실패: {output_path}")

print(f"{output_path} 생성 완료")
'''