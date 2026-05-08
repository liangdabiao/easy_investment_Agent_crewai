# A股智能分析系统 - Go UI 界面

这是一个为Python股票分析系统构建的美观的桌面UI界面，使用Go语言开发。

## 🌟 功能特性

- 🎨 **现代化UI设计**：采用渐变色和动画效果，提供优秀的用户体验
- 📊 **实时分析进度**：通过WebSocket实时显示分析过程和输出
- 🚀 **一键启动**：自动打开浏览器，无需手动访问
- 💼 **跨平台支持**：支持Windows、Linux和macOS
- 🔄 **智能示例**：内置常用股票示例，一键填充
- 📈 **完整报告展示**：清晰展示分析结果

## 📋 系统要求

### 必需条件
- **Python 3.12+**：需要安装Python并配置好股票分析环境
- **Go 1.24+**：用于编译UI程序（如果使用预编译版本则不需要）

### Python环境配置
在运行UI之前，请确保已经安装并配置好Python股票分析系统：

```bash
# 进入股票分析目录
cd ../stock_analysis_a_stock

# 安装依赖
poetry install --no-root
# 或使用 uv
uv sync

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置必要的API密钥
```

## 🚀 快速开始

### 方法1: 使用预编译程序（推荐）

如果提供了预编译版本，直接运行对应平台的可执行文件：

**Windows:**
```bash
stock-analysis-ui-windows-amd64.exe
```

**Linux:**
```bash
chmod +x stock-analysis-ui-linux-amd64
./stock-analysis-ui-linux-amd64
```

**macOS:**
```bash
chmod +x stock-analysis-ui-darwin-amd64  # Intel
# 或
chmod +x stock-analysis-ui-darwin-arm64  # Apple Silicon
./stock-analysis-ui-darwin-amd64
```

程序会自动：
1. 启动Web服务器（默认端口8080）
2. 打开系统默认浏览器访问界面
3. 准备就绪，可以开始分析股票

### 方法2: 从源代码编译

**安装依赖:**
```bash
go mod download
```

**直接运行（开发模式）:**
```bash
go run main.go
```

**编译可执行文件:**

Windows:
```bash
build.bat
```

Linux/macOS:
```bash
chmod +x build.sh
./build.sh
```

## 🎯 使用说明

### 基本使用流程

1. **启动程序**
   - 双击运行可执行文件
   - 或在命令行中运行
   - 浏览器会自动打开 http://localhost:8080

2. **输入股票信息**
   - 公司名称：例如"贵州茅台"
   - 股票代码：例如"600519.SH"
   - 市场类型：选择上交所(SH)、深交所(SZ)或港股(HK)

3. **开始分析**
   - 点击"🚀 开始分析"按钮
   - 实时查看分析进度和输出
   - 等待分析完成

4. **查看结果**
   - 分析完成后，结果会自动显示在页面下方
   - 包含完整的技术分析、财务分析和投资建议

### 快速示例

界面提供了三个内置示例，点击即可快速填充：

- **贵州茅台** (600519.SH) - 上交所白马股
- **平安银行** (000001.SZ) - 深交所金融股
- **腾讯控股** (00700.HK) - 港股科技股

## 🔧 配置说明

### 端口配置

默认使用8080端口，如需更改，设置环境变量：

```bash
# Windows
set PORT=9090
stock-analysis-ui-windows-amd64.exe

# Linux/macOS
export PORT=9090
./stock-analysis-ui-linux-amd64
```

### Python路径

程序会自动查找Python环境，搜索顺序：
1. python3
2. python
3. py

如果自动查找失败，请确保Python在系统PATH中。

## 🏗️ 技术架构

### 后端（Go）
- **Web框架**: Gorilla Mux - HTTP路由
- **WebSocket**: Gorilla WebSocket - 实时通信
- **进程管理**: os/exec - 调用Python分析引擎

### 前端（HTML/CSS/JS）
- **纯HTML5**: 无需额外框架，轻量级
- **现代CSS**: 渐变、动画、响应式设计
- **原生JavaScript**: WebSocket客户端，异步请求

### 通信流程
```
用户界面 <--WebSocket--> Go服务器 <--exec--> Python分析引擎
```

## 📊 API接口

### HTTP端点

- `GET /`: 主页面
- `POST /api/analyze`: 启动分析
- `GET /api/session/{id}`: 获取会话状态

### WebSocket端点

- `WS /ws/{id}`: 实时输出流

### 消息格式

**输出消息:**
```json
{
  "type": "output",
  "data": "分析日志行"
}
```

**状态消息:**
```json
{
  "type": "status",
  "data": "当前状态描述"
}
```

**完成消息:**
```json
{
  "type": "completed",
  "result": "完整的分析报告"
}
```

**错误消息:**
```json
{
  "type": "error",
  "data": "错误描述"
}
```

## 🐛 常见问题

### Q: 运行后浏览器没有自动打开？
A: 手动访问 http://localhost:8080

### Q: 提示"未找到Python环境"？
A: 确保Python已安装并在PATH中，尝试在命令行运行 `python --version`

### Q: 提示"未找到Python分析脚本"？
A: 确保在正确的目录结构中运行，ui文件夹应该与stock_analysis_a_stock在同一层级

### Q: 分析过程卡住不动？
A: 检查Python环境是否正确配置，依赖是否完整安装

### Q: Windows Defender阻止运行？
A: 这是正常的，选择"仍要运行"。这是因为未签名的可执行文件

## 🔒 安全说明

- 程序仅在本地运行（localhost）
- 不会向外部发送任何数据
- 所有分析都在本地Python环境中执行
- WebSocket连接仅限本地访问

## 📝 开发说明

### 项目结构
```
ui/
├── main.go           # 主程序
├── go.mod            # Go模块定义
├── go.sum            # 依赖校验和
├── build.sh          # Linux/macOS构建脚本
├── build.bat         # Windows构建脚本
└── README.md         # 本文档
```

### 修改UI

UI代码内嵌在main.go的`homeHandler`函数中。要修改界面：
1. 编辑`homeHandler`函数中的HTML/CSS/JS
2. 重新编译程序
3. 运行查看效果

### 添加新功能

1. 添加新的API端点到路由
2. 实现对应的handler函数
3. 在前端添加相应的交互逻辑

## 📄 许可证

本项目采用MIT许可证。

## 🙏 致谢

- **CrewAI**: AI Agent框架
- **AKShare**: A股数据源
- **Gorilla**: Go Web工具包

## ⚠️ 免责声明

本系统提供的信息和分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。
