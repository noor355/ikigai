@echo off
REM Start both backend and frontend
echo Starting Ikigai Career Discovery App...
echo.

REM Kill any existing processes on ports 8000 and 3000
echo Cleaning up old processes...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul

REM Wait a moment
timeout /t 2 /nobreak

REM Start backend in a new window
echo Starting Backend (port 8000)...
cd backend
start "Backend Server" cmd /k ".venv\Scripts\activate && python main.py"

REM Wait for backend to start
timeout /t 5 /nobreak

REM Start frontend in a new window
cd ..\frontend
echo Starting Frontend (port 3000)...
start "Frontend Server" cmd /k "npm start"

cd ..
echo.
echo Both services are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.

