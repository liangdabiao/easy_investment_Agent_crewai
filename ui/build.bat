@echo off
REM Build script for A股智能分析系统 UI (Windows)

echo Building A股智能分析系统 UI...

REM Build for Windows
echo Building for Windows (64-bit)...
go build -o stock-analysis-ui-windows-amd64.exe

echo Build complete!
dir stock-analysis-ui-windows-amd64.exe

echo.
echo To run the application, execute:
echo   stock-analysis-ui-windows-amd64.exe
echo.
echo Then open your browser and visit http://localhost:8080
pause
