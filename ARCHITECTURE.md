# 系统架构说明

## 📐 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户（浏览器）                              │
│                  http://localhost:8080                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Go Web服务器 (main.go)                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • HTTP路由 (Gorilla Mux)                           │    │
│  │  • WebSocket服务 (实时通信)                         │    │
│  │  • 会话管理                                         │    │
│  │  • 进程管理                                         │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │ exec.Command
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         Python分析引擎 (PyInstaller打包)                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  cli_entry.py                                       │    │
│  │    ↓                                                │    │
│  │  crew.py (CrewAI)                                   │    │
│  │    ┌──────────────────────────────────┐            │    │
│  │    │  多Agent协作系统                  │            │    │
│  │    │  ├─ A股市场分析师                 │            │    │
│  │    │  ├─ 财务报表专家                  │            │    │
│  │    │  ├─ 市场情绪研究员                │            │    │
│  │    │  └─ A股投资顾问                   │            │    │
│  │    └──────────────────────────────────┘            │    │
│  │    ↓                                                │    │
│  │  tools/ (分析工具)                                  │    │
│  │    ├─ a_stock_data_tool.py (AKShare数据)          │    │
│  │    ├─ financial_tool.py (财务分析)                 │    │
│  │    ├─ market_sentiment_tool.py (情绪分析)         │    │
│  │    └─ calculator_tool.py (计算器)                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  _internal/ (Python运行时 + 依赖)                           │
│    ├─ Python 3.12 运行时                                    │
│    ├─ CrewAI框架                                            │
│    ├─ AKShare数据库                                         │
│    ├─ Pandas/NumPy                                          │
│    └─ 其他依赖包                                            │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 工作流程

### 1. 启动流程

```
用户双击启动
    ↓
Go程序启动
    ↓
启动HTTP服务器 (端口8080)
    ↓
检测Python引擎位置
    ├─ 检查 python_bundle/stock_analysis_engine/
    └─ 如果不存在，回退到系统Python
    ↓
自动打开浏览器
    ↓
显示Web界面
```

### 2. 分析流程

```
用户填写股票信息
    ↓
点击"开始分析"
    ↓
浏览器 → POST /api/analyze → Go服务器
    ↓
创建分析会话
    ↓
建立WebSocket连接
    ↓
Go服务器启动Python进程
    ├─ 使用内置引擎: stock_analysis_engine.exe
    └─ 或系统Python: python cli_entry.py
    ↓
Python引擎执行分析
    ├─ CrewAI调度多个Agent
    ├─ Agent使用各种工具获取数据
    └─ 生成分析报告
    ↓
输出实时传回 (stdout)
    ↓
Go服务器通过WebSocket推送
    ↓
浏览器实时显示进度和日志
    ↓
分析完成，显示最终报告
```

## 📦 打包架构

### 打包前（开发环境）

```
项目根目录/
├── ui/                          (Go Web服务器)
│   ├── main.go
│   ├── go.mod
│   └── go.sum
│
└── stock_analysis_a_stock/      (Python分析系统)
    ├── src/a_stock_analysis/
    │   ├── main.py
    │   ├── crew.py
    │   ├── cli_entry.py         (新增: CLI入口)
    │   ├── config/
    │   └── tools/
    ├── pyproject.toml
    └── build_pyinstaller.spec   (新增: PyInstaller配置)
```

### 打包后（发布版本）

```
A股智能分析系统/                  (发布文件夹)
├── A股智能分析系统.exe           (Go编译后的可执行文件)
│   └── 内含: HTTP服务器 + WebSocket + 进程管理
│
├── python_bundle/                (Python引擎打包)
│   └── stock_analysis_engine/
│       ├── stock_analysis_engine.exe  (PyInstaller打包的Python)
│       │   └── 内含: cli_entry.py入口点
│       │
│       ├── _internal/            (Python运行时环境)
│       │   ├── python312.dll
│       │   ├── base_library.zip
│       │   ├── crewai/           (CrewAI包)
│       │   ├── akshare/          (AKShare包)
│       │   ├── pandas/           (Pandas包)
│       │   └── ... (其他依赖)
│       │
│       └── config/               (配置文件)
│           ├── agents.yaml
│           └── tasks.yaml
│
├── 启动.bat                      (快捷启动脚本)
├── README.txt                    (使用说明)
└── .env.example                  (环境配置模板)
```

## 🔌 通信机制

### HTTP/WebSocket通信

```python
# 浏览器端 (JavaScript)
fetch('/api/analyze', {
    method: 'POST',
    body: JSON.stringify({
        company_name: '贵州茅台',
        stock_code: '600519.SH',
        market: 'SH'
    })
})

# Go服务器端
func analyzeHandler(w http.ResponseWriter, r *http.Request) {
    // 创建会话
    session := createSession(request)
    
    // 后台启动分析
    go runAnalysis(session)
    
    // 返回会话ID
    json.NewEncoder(w).Encode(session.ID)
}

# WebSocket实时推送
ws.send({
    type: 'output',
    data: '正在分析...'
})
```

### 进程间通信

```go
// Go → Python
cmd := exec.Command(
    "stock_analysis_engine.exe",
    "--company", "贵州茅台",
    "--code", "600519.SH",
    "--market", "SH"
)

// 读取Python输出
stdout, _ := cmd.StdoutPipe()
scanner := bufio.NewScanner(stdout)
for scanner.Scan() {
    line := scanner.Text()
    session.broadcast(line)  // 推送到WebSocket
}
```

## 🏗️ 技术栈

### 前端
- **HTML5/CSS3**: 界面设计
- **JavaScript (原生)**: 交互逻辑
- **WebSocket**: 实时通信

### Go后端
- **net/http**: HTTP服务器
- **gorilla/mux**: 路由管理
- **gorilla/websocket**: WebSocket支持
- **os/exec**: 进程管理

### Python引擎
- **CrewAI**: 多Agent协作框架
- **AKShare**: A股数据接口
- **Pandas**: 数据处理
- **LangChain**: LLM集成
- **Pydantic**: 数据验证

### 打包工具
- **PyInstaller**: Python打包
- **Go build**: Go编译
- **UPX**: 可执行文件压缩（可选）

## 🔐 数据流

```
用户输入 (浏览器)
    ↓
JSON数据 (HTTP POST)
    ↓
Go服务器解析
    ↓
命令行参数
    ↓
Python进程启动
    ↓
CrewAI处理
    ├─ Agent 1: 市场分析
    ├─ Agent 2: 财务分析
    ├─ Agent 3: 情绪分析
    └─ Agent 4: 投资建议
    ↓
标准输出 (stdout)
    ↓
Go服务器捕获
    ↓
WebSocket推送
    ↓
浏览器实时显示
```

## 🎯 设计优势

### 1. 关注点分离
- **Go**: 擅长Web服务和并发处理
- **Python**: 擅长数据分析和AI处理

### 2. 易于维护
- 各组件独立开发和测试
- Python引擎可单独运行调试
- Go UI可独立测试

### 3. 灵活部署
- 可以打包成单体应用
- 也可以分布式部署
- 支持容器化

### 4. 良好性能
- Go处理Web请求高效
- Python专注计算密集任务
- 异步处理不阻塞UI

## 📊 性能特征

- **启动时间**: 2-5秒（首次加载Python运行时）
- **内存占用**: 200-500MB（主要是Python运行时）
- **分析耗时**: 30-120秒（取决于网络和LLM响应）
- **并发支持**: 支持多用户同时分析（每个会话独立进程）

## 🔮 扩展可能

### 1. 云端部署
```
用户 → 云端Go服务器 → 容器化Python引擎
```

### 2. 分布式架构
```
负载均衡器 → 多个Go服务器 → Python引擎池
```

### 3. 微服务化
```
前端服务 → API网关 → 分析服务 → 数据服务
```

### 4. 桌面应用
```
Electron/Tauri → 嵌入Go服务器 → Python引擎
```

---

最后更新: 2025-10-14
