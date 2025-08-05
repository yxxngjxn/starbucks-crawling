# 1. 베이스 이미지
FROM python:3.10-slim

# 2. 환경 변수
ENV DEBIAN_FRONTEND=noninteractive
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# 3. 시스템 패키지 설치 (Tesseract + 한국어 데이터)
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-kor \
    libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. 작업 디렉토리
WORKDIR /app

# 5. 코드 복사
COPY . .

# 6. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 7. FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]