@echo off
REM Build script to bundle Python application using PyInstaller

echo ====================================
echo Building Python Bundle with PyInstaller
echo ====================================

REM Check if poetry is available
where poetry >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using Poetry environment...
    poetry run pip install pyinstaller
    poetry run pyinstaller build_pyinstaller.spec --clean
) else (
    REM Check if we're in a virtual environment
    if defined VIRTUAL_ENV (
        echo Using virtual environment...
        pip install pyinstaller
        pyinstaller build_pyinstaller.spec --clean
    ) else (
        echo ERROR: No poetry or virtual environment detected!
        echo Please install dependencies first:
        echo   poetry install --no-root
        echo   OR
        echo   python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
        exit /b 1
    )
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo Python bundle created successfully!
    echo Location: dist\stock_analysis_engine\
    echo ====================================
) else (
    echo.
    echo ====================================
    echo ERROR: Failed to create Python bundle
    echo ====================================
    exit /b 1
)
