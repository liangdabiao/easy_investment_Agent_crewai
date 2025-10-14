@echo off
REM ============================================================================
REM A股智能分析系统 - Windows单体可执行文件构建脚本
REM ============================================================================
REM 本脚本将Python核心和Go UI打包成单个Windows可执行文件包
REM ============================================================================

echo.
echo ========================================
echo  A股智能分析系统 - 单体程序构建
echo ========================================
echo.

REM 检查必要工具
echo [1/5] 检查构建环境...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python未找到，请先安装Python 3.12+
    exit /b 1
)

where go >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Go未找到，请先安装Go 1.24+
    exit /b 1
)

echo ✓ Python和Go环境已就绪

REM 步骤1: 构建Python Bundle
echo.
echo [2/5] 构建Python分析引擎...
cd stock_analysis_a_stock
call build_python_bundle.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python引擎构建失败
    cd ..
    exit /b 1
)
cd ..
echo ✓ Python引擎构建完成

REM 步骤2: 复制Python Bundle到UI目录
echo.
echo [3/5] 准备打包资源...
if not exist "ui\python_bundle" mkdir "ui\python_bundle"
xcopy /E /I /Y "stock_analysis_a_stock\dist\stock_analysis_engine" "ui\python_bundle\stock_analysis_engine"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: 复制Python引擎失败
    exit /b 1
)
echo ✓ Python引擎已复制到UI目录

REM 步骤3: 构建Go UI
echo.
echo [4/5] 构建Go UI程序...
cd ui
go build -ldflags="-s -w" -o stock-analysis-ui-windows-amd64.exe
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Go程序构建失败
    cd ..
    exit /b 1
)
cd ..
echo ✓ Go UI程序构建完成

REM 步骤4: 创建发布包
echo.
echo [5/5] 创建发布包...
if not exist "release" mkdir "release"
if not exist "release\A股智能分析系统" mkdir "release\A股智能分析系统"

REM 复制可执行文件
copy "ui\stock-analysis-ui-windows-amd64.exe" "release\A股智能分析系统\A股智能分析系统.exe"

REM 复制Python引擎
xcopy /E /I /Y "ui\python_bundle" "release\A股智能分析系统\python_bundle"

REM 复制环境变量模板
if exist "stock_analysis_a_stock\src\a_stock_analysis\.env.example" (
    copy "stock_analysis_a_stock\src\a_stock_analysis\.env.example" "release\A股智能分析系统\.env.example"
)

REM 创建启动脚本
echo @echo off > "release\A股智能分析系统\启动.bat"
echo echo 正在启动A股智能分析系统... >> "release\A股智能分析系统\启动.bat"
echo start "" "A股智能分析系统.exe" >> "release\A股智能分析系统\启动.bat"

REM 创建README
echo # A股智能分析系统 > "release\A股智能分析系统\README.txt"
echo. >> "release\A股智能分析系统\README.txt"
echo 使用说明: >> "release\A股智能分析系统\README.txt"
echo 1. 双击"启动.bat"或"A股智能分析系统.exe"启动程序 >> "release\A股智能分析系统\README.txt"
echo 2. 浏览器会自动打开，如果没有，请手动访问 http://localhost:8080 >> "release\A股智能分析系统\README.txt"
echo 3. 在界面中输入股票信息开始分析 >> "release\A股智能分析系统\README.txt"
echo. >> "release\A股智能分析系统\README.txt"
echo 配置说明: >> "release\A股智能分析系统\README.txt"
echo - 如需配置API密钥，请复制.env.example为.env并编辑 >> "release\A股智能分析系统\README.txt"
echo - 环境变量文件应放在程序同目录下 >> "release\A股智能分析系统\README.txt"
echo. >> "release\A股智能分析系统\README.txt"
echo 注意事项: >> "release\A股智能分析系统\README.txt"
echo - 首次运行可能需要几秒钟加载Python引擎 >> "release\A股智能分析系统\README.txt"
echo - 确保系统已安装Microsoft Visual C++ Redistributable >> "release\A股智能分析系统\README.txt"
echo - Windows Defender可能会提示，选择"仍要运行"即可 >> "release\A股智能分析系统\README.txt"

echo ✓ 发布包已创建

REM 完成
echo.
echo ========================================
echo  构建完成！
echo ========================================
echo.
echo 发布包位置: release\A股智能分析系统\
echo.
echo 文件列表:
dir /B "release\A股智能分析系统\"
echo.
echo 您可以将整个"A股智能分析系统"文件夹分发给用户使用
echo.
pause
