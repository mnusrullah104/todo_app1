@echo off
echo ========================================
echo Starting Frontend Only (Development)
echo ========================================
echo.
echo This will start the Next.js frontend only.
echo You need to have the backend running separately.
echo.

cd /d "%~dp0frontend"

echo Installing dependencies...
call npm install

echo.
echo Starting frontend development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.

call npm run dev
