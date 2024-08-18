FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치를 위해 pip 설치 및 업그레이드
RUN pip install --upgrade pip

# requirements.txt 파일이 있는 경우 복사 및 설치
COPY requirements.txt .

RUN pip install -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# uvicorn 명령어로 애플리케이션 실행
CMD ["uvicorn", "core.app_generator:generate_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload", "false", "--factory"]
