# 코드 분석

### 📌 전체 구조 요약

````text
1. 이미지 불러오기
2. SIFT로 특징점 추출
3. FLANN 기반 특징점 매칭
4. 좋은 매칭 추출 (Lowe’s Ratio Test)
5. 호모그래피 계산 (Homography)
6. 이미지 변환 및 합치기 (warpPerspective)
7. 결과 저장 및 표시
````

------------------------------------------------------------------------------------------------------------------------

### 🔍 상세 분석

#### :white_check_mark: 1. 이미지 불러오기

```python
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')
```

- `cv2.imread()` : 지정한 경로에서 이미지를 읽어오는 함수
- 반환값은 Numpy 배열 형식의 이미지 데이터
- `img1` : 기준 이미지(왼쪽 이미지로 유지될 예정)
- `img2` : 변환될 이미지(오른쪽에서 이어붙여질 이미지)



#### :white_check_mark: 2.SIFT로 특징점 추출

```python
sift = cv2.SIFT_create()
```

- `SIFT` : Scale-Invariant Feature Transform
- 이미지에서 독립적이고 다양한 크기, 회전, 조명 변화에도 강인한 특징점 추출 알고리즘

````python
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
````

- `detectAndCompute()` : 두 가지를 한번에 처리
  - `kp(keypoints)` : 이미지에서 눈에 띄는 점의 위치(ex : 모서리, 점 등)
  - `des(descriptors)` : 각 keypoint 주변 특징을 숫자 벡터로 표현

:arrow_forward: SIFT는 keypoint 간 정합 판단의 기준이 되는 핵심 데이터를 만듬.



## ✅ 3. FLANN 기반 특징점 매칭

```python
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
```

- `FLANN` : Fast Library for Approximate Nearest Neighbors
- 고차원 벡터 공간에서 빠르게 비슷한 것을 찾아주는 알고리즘
- `KDTREE`는 벡터를 트리 구조로 정렬해서 검색 속도를 높임

```python
search_params = dict(checks=50)
```

- `checks`: 탐색 시 비교하는 횟수 (많을수록 정확, 적을수록 빠름)

```python
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
```

- 특징 벡터끼리의 거리 계산을 통해 매칭 시도
- `knnMatch(..., k=2)`: 각 특징점마다 가까운 2개의 후보를 반환



## ✅ 4. 좋은 매칭 추출 (Lowe’s Ratio Test)

```python
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)
```

- Lowe’s 논문에서 제안된 조건
- 두 번째로 가까운 점보다 훨씬 가까운 점일 때만 신뢰함
- `distance`: 두 벡터 간 거리 (작을수록 더 비슷)

:arrow_forward: 이 과정을 거치면 이상치(오탐) 제거 가능



## ✅ 5. 호모그래피 계산

```python
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
```

- `queryIdx`: 기준 이미지(`img1`)에서 매칭된 특징점의 인덱스
- `trainIdx`: 변환될 이미지(`img2`)에서의 인덱스
- `.pt`: keypoint의 `(x, y)` 좌표 반환

```python
H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
```

- Homography 행렬 H: 두 이미지의 좌표계를 일치시키는 3x3 변환 행렬
- `cv2.RANSAC`: 이상치를 배제하면서 안정적인 변환을 찾아주는 알고리즘
- `5.0`: 허용 오차 (픽셀 단위)

:arrow_forward: H를 구하면 `img2`를 `img1`의 시점에 맞게 정확하게 변환 가능



## ✅ 6. 이미지 변환 및 스티칭

```python
height, width, _ = img1.shape
```

- `img1`의 세로, 가로, 채널 수 추출

```python
result = cv2.warpPerspective(img2, H, (width * 2, height))
```

- `warpPerspective()`: `img2`를 Homography 행렬 H를 기반으로 변형
- `width * 2`: 결과 이미지의 폭을 두 배로 확보 (여유 공간)
- 이 시점에서 `img2`는 `img1`의 시점에 맞게 정렬됨

```python
result[0:img1.shape[0], 0:img1.shape[1]] = img1
```

- `img1`을 왼쪽 영역에 직접 덮어쓰기 → 블렌딩 없이 복사
- 자연스럽지 않은 경계가 생기는 이유가 여기 있음



## ✅ 7. 결과 저장 및 출력

```python
cv2.imwrite("stitched_result.jpg", result)
```

- 결과 이미지를 `stitched_result.jpg`로 저장

```python
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

- 결과 이미지 띄우기
- 아무 키나 누르면 창 닫기



## 📦 정리

| 구간                | 기능 요약                                |
| ------------------- | ---------------------------------------- |
| SIFT                | 각 이미지의 특징점 추출                  |
| FLANN               | 두 이미지 간 유사한 특징점 찾기          |
| RANSAC + Homography | 이상치를 제거하며 정합 행렬 계산         |
| warpPerspective     | 두 번째 이미지를 기준 이미지에 맞게 변형 |
| 결과 합치기         | 두 이미지를 이어붙여 최종 이미지 생성    |
