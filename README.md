# 🧵 OpenCV를 이용한 이미지 스티칭 프로젝트

이 프로젝트는 Python과 OpenCV를 사용하여 **두 장의 겹치는 이미지를 하나의 파노라마 이미지로 자연스럽게 이어붙이는 예제**입니다.

## 📌 주요 기능

- SIFT(Scale-Invariant Feature Transform)를 활용한 특징점 추출
- FLANN 기반 특징점 매칭
- 호모그래피(Homography) 계산을 통한 정렬
- 이미지 결합 및 블렌딩 처리
- OpenCV의 `cv2.Stitcher_create()`를 이용한 자동 스티칭 기능

## 🖼 예시 결과

<p align="center">
  <img src="stitched_result.jpg" width="600" />
</p>

## 🚀 실행 방법

1. 레포지토리 클론:
   ```bash
   git clone https://github.com/lee-jin-wo0/Image_Stitching.git
   cd Image_Stitching
   
필수 라이브러리 설치:
pip install opencv-python numpy
프로젝트 폴더에 image1.jpg, image2.jpg 두 장의 겹치는 이미지를 넣습니다.

실행:
python main.py
결과물은 stitched_result.jpg로 저장됩니다.

📂 폴더 구조
Image_Stitching/

├── image1.jpg

├── image2.jpg

├── main.py

├── stitched_result.jpg

├── .gitignore

└── README.md

⚙ 필요 환경

Python 3.7 이상

OpenCV 4.x 이상

NumPy

---
