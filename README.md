# A股智能分析系统

基于AKShare和CrewAI的A股智能分析平台，通过多Agent协作提供专业的A股投资分析。

## 🚀 项目特色

- **📊 全面的A股数据分析**：实时行情、财务数据、资金流向、市场情绪
- **🤖 多Agent协作**：4个专业化AI角色协同工作
- **🇨🇳 A股市场特色**：针对中国股市特点优化分析
- **📈 专业分析工具**：基于AKShare的专业数据源
- **🎯 智能投资建议**：综合分析提供投资决策参考

## 🏗️ 系统架构

### 四大专业Agent

1. **📈 A股市场分析师**：技术面、政策面、资金面分析
2. **💰 财务报表专家**：财务比率、趋势分析、同业对比
3. **😊 市场情绪研究员**：资金流向、市场情绪、政策影响
4. **💼 A股投资顾问**：综合分析、投资策略、风险控制

### 专业工具集

- **📊 A股数据工具**：实时行情、历史数据、财务指标
- **🧮 财务分析工具**：深度财务分析、同业对比
- **😐 市场情绪工具**：资金流向、新闻情绪、技术情绪
- **🔢 计算器工具**：安全数学计算

## 📦 安装和使用

### 环境要求

- Python 3.12+
- 推荐使用Poetry管理依赖

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd stock_analysis_a_stock
```

2. **安装依赖**
```bash
poetry install --no-root
```

或者： Install dependencies with UV 
   ```bash
   uv sync  # Installs all dependencies and creates virtual environment
   ```


3. **配置环境**
```bash
cp .env.example .env
# 编辑.env文件配置必要参数
```

4. **运行分析**
```bash
# 默认分析腾讯控股
poetry run python src/a_stock_analysis/main.py

# 或使用安装的脚本
poetry run a_stock_analysis
```

### 分析示例

系统默认分析腾讯控股（00700.HK），您可以修改 `main.py` 中的参数来分析其他股票：

```python
inputs = {
    'company_name': '贵州茅台',
    'stock_code': '600519.SH',  # A股股票代码
    'market': 'SH'               # SH=上交所, SZ=深交所, HK=港股
}
```

### 支持的股票代码格式

- **上交所A股**：`600519.SH`
- **深交所A股**：`000001.SZ`
- **港股**：`00700.HK`

## 🔧 自定义配置

### 切换AI模型

在 `src/a_stock_analysis/crew.py` 中，您可以：

```python
# 使用Ollama本地模型（默认）
from langchain.llms import Ollama
llm = Ollama(model="llama3.1")

# 或使用OpenAI GPT模型
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model='gpt-4')
```

### 修改Agent配置

编辑 `config/agents.yaml` 来调整各Agent的角色、目标和背景故事。

### 自定义分析任务

编辑 `config/tasks.yaml` 来修改分析任务的具体要求和输出格式。

## 📋 功能特性

### 数据获取能力

- ✅ 实时行情数据
- ✅ 历史K线数据
- ✅ 财务报表数据
- ✅ 资金流向数据
- ✅ 行业板块数据
- ✅ 市场情绪指标

### 分析维度

- 🔍 **技术分析**：K线形态、均线系统、技术指标
- 📊 **财务分析**：财务比率、趋势分析、同业对比
- 💧 **资金分析**：主力资金、北向资金、散户资金
- 😊 **情绪分析**：市场情绪、政策影响、热点追踪
- 🎯 **投资建议**：评级目标、策略建议、风险控制

### A股特色功能

- 🏢 **政策影响分析**：关注中国政策对股市的影响
- 📉 **涨跌停分析**：考虑A股涨跌停限制的影响
- 🇨🇳 **散户情绪**：分析A股散户投资者的心理特征
- 💰 **资金轮动**：追踪中国特色的资金流向规律

## ⚠️ 风险提示

- 本系统仅供学习研究使用，不构成投资建议
- A股市场风险较高，投资需谨慎
- 建议结合多种分析方法做出投资决策
- 过往业绩不代表未来表现

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证。

---

**免责声明**：本系统提供的信息和分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。