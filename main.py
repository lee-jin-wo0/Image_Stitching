import cv2
import numpy as np

# 이미지 불러오기
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')

# SIFT로 특징점 추출
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN 매칭
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# 좋은 매칭 추출 (Lowe’s ratio test)
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# 호모그래피 계산
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

# 이미지 변환 및 스티칭
height, width, _ = img1.shape
result = cv2.warpPerspective(img2, H, (width * 2, height))
result[0:img1.shape[0], 0:img1.shape[1]] = img1

# 결과 저장 및 보기
cv2.imwrite("stitched_result.jpg", result)
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
