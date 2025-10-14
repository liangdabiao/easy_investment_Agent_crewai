@echo off
REM Quick start script for A股智能分析系统 UI (Windows)

echo ==================================
echo A股智能分析系统 UI
echo ==================================
echo.

REM Check if binary exists
if not exist "stock-analysis-ui-windows-amd64.exe" (
    echo 可执行文件不存在，正在编译...
    go build -o stock-analysis-ui-windows-amd64.exe main.go
    if errorlevel 1 (
        echo 编译失败！请检查Go环境和依赖。
        pause
        exit /b 1
    )
    echo 编译成功！
    echo.
)

echo 启动UI服务器...
echo 访问地址: http://localhost:8080
echo 浏览器将自动打开
echo 按 Ctrl+C 停止服务器
echo.

stock-analysis-ui-windows-amd64.exe
