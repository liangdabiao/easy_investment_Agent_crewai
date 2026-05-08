# 故障排除指南

本文档帮助您解决构建和运行过程中可能遇到的问题。

## 🔍 快速诊断

运行问题？首先确定问题出在哪个阶段：

```
┌─────────────────┐
│  构建Python引擎  │ → PyInstaller相关问题
├─────────────────┤
│   编译Go程序    │ → Go编译相关问题
├─────────────────┤
│   组织发布包    │ → 文件路径/权限问题
├─────────────────┤
│   运行程序      │ → 运行时环境问题
└─────────────────┘
```

## 🐛 常见问题及解决方案

### 构建阶段问题

#### 问题1: PyInstaller打包失败

**症状:**
```bash
poetry run pyinstaller build_pyinstaller.spec
ERROR: Cannot import module 'xxx'
```

**原因:**
- 缺少Python依赖
- Poetry环境未激活
- 某些模块隐藏导入未配置

**解决方案:**

**步骤1: 验证环境**
```bash
cd stock_analysis_a_stock

# 确认Poetry环境
poetry env info

# 重新安装依赖
poetry install --no-root

# 验证关键依赖
poetry run python -c "import crewai; import akshare; print('OK')"
```

**步骤2: 查看详细日志**
```bash
poetry run pyinstaller build_pyinstaller.spec --log-level DEBUG > build.log 2>&1
# 查看 build.log 文件找出具体错误
```

**步骤3: 添加隐藏导入**

如果提示 `No module named 'xxx'`，编辑 `build_pyinstaller.spec`:

```python
hiddenimports=[
    'crewai',
    'crewai.tools',
    'crewai_tools',
    'akshare',
    'xxx',  # 添加缺失的模块
],
```

**步骤4: 清理缓存重试**
```bash
# 清理之前的构建
rm -rf build/ dist/

# 重新打包
poetry run pyinstaller build_pyinstaller.spec --clean
```

#### 问题2: Go编译失败

**症状:**
```bash
go build -o app.exe
# 或
undefined: someFunction
```

**原因:**
- Go版本过低
- 依赖未下载
- 代码语法错误

**解决方案:**

**步骤1: 检查Go版本**
```bash
go version
# 应该是 go1.24 或更高
```

如果版本过低，从 https://golang.org/dl/ 下载最新版。

**步骤2: 更新依赖**
```bash
cd ui

# 清理模块缓存
go clean -modcache

# 重新下载依赖
go mod download

# 整理依赖
go mod tidy
```

**步骤3: 验证代码**
```bash
# 运行测试
go test ./...

# 检查语法
go vet ./...
```

**步骤4: 清理重编译**
```bash
go clean -cache
go build -v -o test.exe
```

#### 问题3: 交叉编译Windows版本失败（Linux/macOS）

**症状:**
```bash
GOOS=windows GOARCH=amd64 go build
# 某些CGO相关错误
```

**原因:**
- 缺少交叉编译工具链
- CGO依赖问题

**解决方案:**

**禁用CGO**（如果不需要）:
```bash
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o app.exe
```

**安装mingw**（如果需要CGO）:
```bash
# Ubuntu/Debian
sudo apt-get install gcc-mingw-w64

# macOS
brew install mingw-w64

# 编译
CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 go build
```

#### 问题4: 文件路径错误

**症状:**
```
ERROR: cannot find file: src/a_stock_analysis/.env.example
```

**原因:**
文件名不匹配（.env.example vs env.example）

**解决方案:**

检查文件实际名称:
```bash
ls -la stock_analysis_a_stock/src/a_stock_analysis/ | grep env
```

更新脚本中的路径引用。

### 运行阶段问题

#### 问题5: 双击exe没有反应

**症状:**
双击 `A股智能分析系统.exe`，没有任何窗口或浏览器打开。

**诊断:**

**步骤1: 命令行运行**
```bash
cd "release/A股智能分析系统"
"A股智能分析系统.exe"
# 查看输出的错误信息
```

**步骤2: 检查端口占用**
```bash
# Windows
netstat -ano | findstr :8080

# 如果8080被占用，设置其他端口
set PORT=9090
"A股智能分析系统.exe"
```

**步骤3: 检查Python引擎**
```bash
# 验证Python引擎存在
dir python_bundle\stock_analysis_engine\stock_analysis_engine.exe

# 尝试直接运行Python引擎测试
cd python_bundle\stock_analysis_engine
stock_analysis_engine.exe --company 测试 --code 600519.SH --market SH
```

#### 问题6: 提示"未找到Python引擎"

**症状:**
```
Go程序启动，但提示：未找到Python分析脚本
```

**原因:**
- python_bundle目录结构不正确
- 路径配置错误

**解决方案:**

**验证目录结构:**
```bash
A股智能分析系统/
├── A股智能分析系统.exe
└── python_bundle/
    └── stock_analysis_engine/
        ├── stock_analysis_engine.exe  ← 必须存在
        └── _internal/
```

**手动复制修复:**
```bash
# 如果缺失，重新复制
mkdir -p "release/A股智能分析系统/python_bundle"
cp -r ui/python_bundle/stock_analysis_engine "release/A股智能分析系统/python_bundle/"
```

#### 问题7: Windows Defender阻止运行

**症状:**
Windows提示"Windows保护了你的电脑"或"此应用已被阻止"。

**原因:**
未签名的可执行文件被SmartScreen过滤。

**临时解决方案（用户端）:**
1. 点击"更多信息"
2. 点击"仍要运行"

**永久解决方案（开发端）:**
1. **获取代码签名证书**
   - 从DigiCert、Sectigo等CA购买
   - 价格约$200-500/年

2. **签名可执行文件**
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com "A股智能分析系统.exe"
   ```

3. **提交到Microsoft SmartScreen**
   - 需要积累使用量
   - 通常需要几周到几个月

**替代方案:**
```bash
# 添加到Windows Defender排除列表
# 以管理员身份运行PowerShell
Add-MpPreference -ExclusionPath "C:\path\to\A股智能分析系统"
```

#### 问题8: 缺少DLL文件

**症状:**
```
The code execution cannot proceed because python312.dll was not found.
```

**原因:**
- PyInstaller打包不完整
- 缺少Visual C++ Redistributable

**解决方案:**

**步骤1: 重新打包Python引擎**
```bash
cd stock_analysis_a_stock
poetry run pyinstaller build_pyinstaller.spec --clean
```

**步骤2: 安装VC++ Redistributable**

下载并安装: https://aka.ms/vs/17/release/vc_redist.x64.exe

**步骤3: 检查打包目录**
```bash
# python312.dll应该在这里
dir dist\stock_analysis_engine\_internal\python312.dll
```

#### 问题9: 分析时报错"ModuleNotFoundError"

**症状:**
Go程序启动成功，但点击"开始分析"后Python引擎报错缺少模块。

**原因:**
PyInstaller未包含某些动态导入的模块。

**解决方案:**

**步骤1: 查看错误日志**
在Go程序终端中查看完整错误。

**步骤2: 添加到hiddenimports**
编辑 `build_pyinstaller.spec`:
```python
hiddenimports=[
    # ... 现有的
    'missing_module_name',  # 添加缺失的模块
],
```

**步骤3: 重新打包**
```bash
cd stock_analysis_a_stock
poetry run pyinstaller build_pyinstaller.spec --clean
```

**步骤4: 使用--collect-all（最后手段）**
```bash
poetry run pyinstaller build_pyinstaller.spec --collect-all missing_package
```

#### 问题10: 无法连接网络/API

**症状:**
分析时提示网络错误或API调用失败。

**原因:**
- 防火墙阻止
- API密钥未配置
- 网络连接问题

**解决方案:**

**步骤1: 配置环境变量**
```bash
# 复制环境变量模板
cd "release/A股智能分析系统"
copy .env.example .env

# 编辑.env，设置API密钥
notepad .env
```

**步骤2: 检查防火墙**
```bash
# Windows防火墙
# 以管理员身份运行
netsh advfirewall firewall add rule name="A股智能分析系统" dir=in action=allow program="C:\path\to\A股智能分析系统.exe" enable=yes
```

**步骤3: 测试网络连接**
```bash
# 测试AKShare能否访问
python -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"
```

## 🔬 调试技巧

### 启用详细日志

**Go程序:**
```go
// 在main.go中
log.SetFlags(log.LstdFlags | log.Lshortfile)
```

**Python引擎:**
```bash
# 直接运行查看输出
python_bundle\stock_analysis_engine\stock_analysis_engine.exe --company 测试 --code 600519.SH --market SH
```

### 使用开发模式

如果打包版本有问题，尝试开发模式：

```bash
# 1. 启动Python服务（可选）
cd stock_analysis_a_stock
poetry run python src/a_stock_analysis/main.py

# 2. 启动Go UI（会自动回退到系统Python）
cd ui
go run main.go
```

### 逐步测试

**测试1: Python引擎独立运行**
```bash
cd stock_analysis_a_stock/dist/stock_analysis_engine
stock_analysis_engine.exe --company 贵州茅台 --code 600519.SH --market SH
```

**测试2: Go程序连接测试**
```bash
cd ui
go run main.go
# 在浏览器中测试
```

**测试3: 集成测试**
```bash
cd release/A股智能分析系统
"A股智能分析系统.exe"
```

## 📞 获取帮助

如果以上方法都无法解决您的问题：

1. **查看日志**
   - Go程序终端输出
   - Python引擎错误信息
   - 浏览器开发者工具控制台

2. **收集信息**
   - 操作系统版本
   - Python版本
   - Go版本
   - 完整错误信息
   - 复现步骤

3. **提交Issue**
   - GitHub Issues
   - 包含上述所有信息
   - 附上日志文件

4. **查阅文档**
   - [打包指南.md](打包指南.md)
   - [BUILD_GUIDE.md](BUILD_GUIDE.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)

## 🎯 预防性措施

### 构建前检查

- [ ] Python 3.12+已安装
- [ ] Go 1.24+已安装
- [ ] Poetry已配置
- [ ] 所有依赖已安装
- [ ] 磁盘空间充足（至少5GB）

### 构建后验证

- [ ] Python引擎可独立运行
- [ ] Go程序可独立启动
- [ ] 目录结构正确
- [ ] 所有文件已包含
- [ ] 在干净的Windows系统测试

### 发布前测试

- [ ] 完整功能测试
- [ ] 多个股票分析测试
- [ ] 错误处理测试
- [ ] 长时间运行测试
- [ ] 不同Windows版本测试

---

**最后更新**: 2025-10-14  
**维护**: 持续更新中

如有新问题，欢迎贡献到本文档！
