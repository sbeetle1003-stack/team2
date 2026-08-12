import cv2
import cv2.aruco as aruco

# 1. 딕셔너리 불러오기
# (cv2.aruco가 아닌 직접 aruco 모듈에서 딕셔너리를 가져옵니다)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# 2. 0번부터 8번까지 9개의 마커 생성
for i in range(9):
    # generateImageMarker 대신, 구버전과 신버전 모두 호환되는 drawMarker 사용
    # drawMarker(dictionary, markerId, sidePixels)
    marker_image = aruco.drawMarker(dictionary, i, 200)
    
    # 3. 파일 저장
    filename = f'aruco_marker_{i}.png'
    cv2.imwrite(filename, marker_image)
    print(f"생성 완료: {filename}")

print("ArUco 마커 이미지 0~8번 생성 완료!")