@echo off
echo ========================================
echo Starting Phase 2 Todo App (Development)
echo ========================================
echo.

REM Check if Docker is running (for database)
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo.
    echo Please start Docker Desktop first.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo [1/4] Starting PostgreSQL database...
cd /d "%~dp0"
docker-compose up -d db
timeout /t 5 /nobreak >nul

echo.
echo [2/4] Checking database health...
timeout /t 5 /nobreak >nul

echo.
echo [3/4] Starting Backend (FastAPI)...
start "Todo Backend" cmd /k "cd /d %~dp0backend && echo Installing dependencies... && pip install -r requirements.txt && echo Running migrations... && alembic upgrade head && echo Starting backend server... && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo [4/4] Starting Frontend (Next.js)...
start "Todo Frontend" cmd /k "cd /d %~dp0frontend && echo Installing dependencies... && npm install && echo Starting frontend server... && npm run dev"

echo.
echo ========================================
echo ✅ Servers Starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
docker-compose down
echo Done!
