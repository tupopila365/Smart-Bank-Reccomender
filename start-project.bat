@echo off
echo ========================================
echo SmartBank Recommender - Quick Start
echo ========================================
echo.

echo Starting backend services with Docker...
docker-compose up -d

echo.
echo Waiting for services to be healthy...
timeout /t 10 /nobreak >nul

echo.
echo Checking service health...
docker ps

echo.
echo ========================================
echo Backend Services Started!
echo ========================================
echo.
echo ML Service:  http://localhost:8000
echo Backend API: http://localhost:3000
echo.
echo To start the mobile app:
echo   cd mobile
echo   npm start
echo.
echo To stop services:
echo   docker-compose down
echo.
echo ========================================
pause
