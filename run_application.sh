#!/bin/bash

# Docker Compose 실행
echo "Starting Docker Compose..."
docker-compose -f docker-compose.yml up --build -d
if [ $? -ne 0 ]; then
    echo "Docker Compose failed to start."
    exit 1
fi

# FastAPI 앱 실행
echo "Starting FastAPI app..."
python3 app/main.py &
if [ $? -ne 0 ]; then
    echo "Failed to start FastAPI app."
    exit 1
fi

# Celery 워커 실행
echo "Starting Celery worker..."
cd inference && celery -A worker worker --loglevel=info --pool=solo &
if [ $? -ne 0 ]; then
    echo "Failed to start Celery worker."
    exit 1
fi

echo "All services started successfully."
