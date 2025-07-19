FROM python:3.9-slim

# 1. 시스템 패키지 업데이트 및 tesseract 설치
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. 작업 디렉토리 및 파이썬 의존성 설치
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 소스 복사 및 서버 실행
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]