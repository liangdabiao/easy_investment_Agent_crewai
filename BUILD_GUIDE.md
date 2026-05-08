# 构建指南 - 创建Windows单体可执行文件

本指南说明如何将A股智能分析系统（Go + Python混合应用）打包成单个Windows可执行文件包。

## 📋 系统架构

```
┌─────────────────────────────────────┐
│     Windows 单体发布包              │
├─────────────────────────────────────┤
│                                     │
│  A股智能分析系统.exe (Go)           │  ← 主程序，提供Web UI
│       ↓                             │
│  python_bundle/                     │  ← 内置Python分析引擎
│    └── stock_analysis_engine/       │
│         ├── stock_analysis_engine.exe│  ← PyInstaller打包的Python
│         ├── _internal/              │  ← Python运行时和依赖
│         └── config/                 │  ← 配置文件
│                                     │
└─────────────────────────────────────┘
```

## 🎯 设计目标

1. **单体分发**: 所有依赖打包在一个文件夹中
2. **无需安装Python**: Python运行时内置在包中
3. **一键启动**: 双击即可运行，浏览器自动打开
4. **跨平台构建**: 可在Linux/macOS上交叉编译Windows版本

## 🛠️ 构建要求

### 必需软件

- **Python 3.12+**: 用于构建Python bundle
- **Go 1.24+**: 用于编译Go UI程序
- **PyInstaller**: Python打包工具（脚本会自动安装）

### 可选但推荐

- **Poetry**: Python依赖管理（推荐）
- **UPX**: 可执行文件压缩工具（减小体积）

## 🚀 快速构建

### Windows系统

```bash
# 一键构建
build_windows_exe.bat
```

### Linux/macOS系统（交叉编译）

```bash
# 赋予执行权限
chmod +x build_windows_exe.sh

# 执行构建
./build_windows_exe.sh
```

## 📝 构建步骤详解

### 步骤1: 准备Python环境

首先确保Python依赖已安装：

```bash
cd stock_analysis_a_stock
poetry install --no-root
# 或使用 uv sync
```

### 步骤2: 构建Python Bundle

使用PyInstaller将Python应用打包：

```bash
cd stock_analysis_a_stock
# Windows
build_python_bundle.bat

# Linux/macOS
./build_python_bundle.sh
```

这将创建：
- `dist/stock_analysis_engine/stock_analysis_engine.exe`
- `dist/stock_analysis_engine/_internal/` (Python运行时)
- `dist/stock_analysis_engine/config/` (配置文件)

### 步骤3: 复制到UI目录

将Python bundle复制到Go UI目录：

```bash
# Windows
xcopy /E /I stock_analysis_a_stock\dist\stock_analysis_engine ui\python_bundle\stock_analysis_engine

# Linux/macOS
cp -r stock_analysis_a_stock/dist/stock_analysis_engine ui/python_bundle/
```

### 步骤4: 构建Go程序

编译Go UI程序：

```bash
cd ui

# Windows本地编译
go build -ldflags="-s -w" -o stock-analysis-ui-windows-amd64.exe

# Linux/macOS交叉编译为Windows
GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o stock-analysis-ui-windows-amd64.exe
```

### 步骤5: 创建发布包

组织文件结构：

```
release/
└── A股智能分析系统/
    ├── A股智能分析系统.exe        # 重命名的Go程序
    ├── 启动.bat                    # 快捷启动脚本
    ├── README.txt                  # 使用说明
    ├── .env.example               # 环境变量模板
    └── python_bundle/             # Python引擎
        └── stock_analysis_engine/
            ├── stock_analysis_engine.exe
            └── _internal/
```

## 🔧 高级配置

### 减小包体积

1. **使用UPX压缩**:
   ```bash
   # 安装UPX
   # Windows: choco install upx
   # Linux: apt install upx / yum install upx
   # macOS: brew install upx
   
   # PyInstaller会自动使用UPX（如果已安装）
   ```

2. **排除不必要的库**:
   编辑 `stock_analysis_a_stock/build_pyinstaller.spec`，在 `excludes` 中添加不需要的模块。

3. **优化Go编译**:
   ```bash
   go build -ldflags="-s -w" -trimpath
   ```

### 添加图标

**Windows可执行文件图标**:

1. 准备 `.ico` 文件
2. 修改Go构建命令：
   ```bash
   go build -ldflags="-s -w -H windowsgui" -o app.exe
   ```

3. 或使用 `windres`:
   ```bash
   windres -o icon.syso icon.rc
   go build -o app.exe
   ```

### 数字签名（可选）

对Windows可执行文件进行代码签名：

```bash
# 使用signtool（Windows SDK）
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com app.exe
```

## 🧪 测试发布包

### 基本功能测试

1. 双击 `A股智能分析系统.exe` 或 `启动.bat`
2. 验证浏览器自动打开
3. 测试分析功能
4. 检查日志输出

### 兼容性测试

在不同Windows版本上测试：
- Windows 10
- Windows 11
- Windows Server 2019+

### 性能测试

- 启动时间
- 内存占用
- 分析速度

## 📦 分发建议

### 压缩发布包

```bash
# 创建ZIP压缩包
7z a -tzip A股智能分析系统-v1.0.zip release\A股智能分析系统\

# 或使用PowerShell
Compress-Archive -Path "release\A股智能分析系统" -DestinationPath "A股智能分析系统-v1.0.zip"
```

### 发布清单

- [ ] 测试所有核心功能
- [ ] 检查README文档完整性
- [ ] 验证.env.example模板
- [ ] 测试启动脚本
- [ ] 病毒扫描（避免误报）
- [ ] 创建MD5/SHA256校验和
- [ ] 编写版本更新日志

### 版本命名

建议格式：`A股智能分析系统-v主版本.次版本.修订版本-平台.zip`

示例：
- `A股智能分析系统-v1.0.0-windows-amd64.zip`
- `A股智能分析系统-v1.1.0-windows-amd64.zip`

## 🐛 常见问题

### Q1: PyInstaller打包失败？

**原因**: 缺少某些依赖或模块无法找到

**解决方案**:
1. 确保所有Python依赖已安装
2. 检查 `build_pyinstaller.spec` 中的 `hiddenimports`
3. 尝试使用 `--collect-all` 参数
4. 查看详细日志：`pyinstaller --log-level DEBUG build_pyinstaller.spec`

### Q2: 运行时提示"未找到DLL"？

**原因**: 缺少Visual C++ Redistributable

**解决方案**:
1. 用户需要安装 [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. 或在打包时包含这些DLL（不推荐，可能违反许可）

### Q3: Windows Defender阻止运行？

**原因**: 未签名的可执行文件被标记为可疑

**解决方案**:
1. 用户选择"更多信息" -> "仍要运行"
2. 获取代码签名证书对程序签名
3. 提交到Microsoft SmartScreen白名单

### Q4: 包体积过大？

**原因**: Python运行时和依赖库较大

**解决方案**:
1. 使用UPX压缩
2. 排除不必要的依赖
3. 使用虚拟环境减少依赖
4. 考虑分离大型数据文件

### Q5: 在Linux/macOS上构建Windows版本失败？

**原因**: 交叉编译配置问题

**解决方案**:
1. 确保安装了交叉编译工具链
2. Python部分需要在Windows环境或Wine中构建
3. 考虑使用Docker容器构建

## 🔒 安全注意事项

1. **不要在代码中硬编码敏感信息**
   - API密钥应通过.env文件配置
   - 提供.env.example作为模板

2. **验证用户输入**
   - 股票代码格式验证
   - 防止命令注入

3. **依赖更新**
   - 定期更新Python和Go依赖
   - 检查安全漏洞

4. **代码签名**
   - 建议获取代码签名证书
   - 提高用户信任度

## 📚 参考资源

- [PyInstaller文档](https://pyinstaller.org/)
- [Go交叉编译](https://golang.org/doc/install/source#environment)
- [Windows打包最佳实践](https://docs.microsoft.com/en-us/windows/apps/package/)

## 🎯 后续优化方向

1. **自动更新机制**: 添加版本检查和自动更新功能
2. **安装程序**: 使用NSIS或WiX创建安装向导
3. **便携版本**: 创建完全便携的免安装版本
4. **云端部署**: 支持云服务器部署
5. **Docker容器**: 提供容器化部署方案

## 💡 贡献

欢迎提交改进建议和问题反馈！

---

**最后更新**: 2025年10月
