# A股智能分析系统

基于AKShare的A股智能分析系统，使用CrewAI多Agent协作进行股票数据分析与决策支持。

## 项目概述

本系统利用先进的多Agent协作框架(CrewAI)和丰富的A股市场数据(AKShare)，构建了一个全面的股票分析平台。系统通过多个专业Agent协同工作，提供从数据获取、财务分析到市场情绪研判的全流程服务，帮助投资者做出更明智的投资决策。

## 功能特性

### 核心功能

- **A股数据获取**：获取A股股票的实时行情、历史K线数据、财务指标和板块数据
- **财务分析**：深度分析公司财务报表，计算关键财务比率，识别财务趋势和风险
- **市场情绪分析**：跟踪资金流向、分析新闻情绪和技术面指标，综合评估市场情绪
- **智能计算支持**：提供安全的数学计算工具，辅助投资决策过程中的数值计算

### 工具详情

1. **A股数据获取工具**
   - 支持获取实时行情数据（最新价、涨跌幅、成交量等）
   - 提供历史日线数据（支持指定时间范围）
   - 可获取财务数据（包括财务报表主要指标）
   - 支持板块数据查询（行业分类和板块行情）

2. **财务分析工具**
   - 财务比率分析：计算盈利能力、偿债能力、运营能力等核心比率
   - 趋势分析：分析财务指标的历史变化趋势
   - 同业对比：与同行业公司进行财务指标对比分析

3. **市场情绪分析工具**
   - 资金流向分析：监控主力资金流入流出情况
   - 新闻情绪分析：抓取并分析相关新闻的情感倾向
   - 技术情绪分析：基于技术指标评估市场情绪

4. **计算器工具**
   - 支持基本数学运算（加减乘除）
   - 提供高级运算功能（指数、对数等）
   - 安全的表达式解析，防止代码注入

## 依赖环境

- Python 3.12+（最高支持3.13）
- CrewAI 0.152.0+（多Agent协作框架）
- AKShare 1.12.0+（A股数据接口库）
- Pydantic 2.0.0+（数据验证库）
- Pandas 2.0.0+（数据处理库）
- NumPy 1.24.0+（科学计算库）
- 其他依赖详见pyproject.toml

## 安装步骤

### 方法一：使用Poetry（推荐）

```bash
# 克隆仓库
git clone <repository_url>
cd crewAI-examples-main/crews/stock_analysis_a_stock/src/a_stock_analysis

# 安装poetry（如果尚未安装）
pip install poetry

# 使用poetry安装依赖
poetry install

# 配置环境变量
copy .env.example .env
# 编辑.env文件，填写必要的API密钥
```

### 方法二：使用pip

```bash
# 克隆仓库
git clone <repository_url>
cd crewAI-examples-main/crews/stock_analysis_a_stock/src/a_stock_analysis

# 使用pip安装依赖
pip install -e .

# 配置环境变量
copy .env.example .env
# 编辑.env文件，填写必要的API密钥
```

## 使用方法

### 基本使用

```bash
# 使用Python直接运行
python main.py

# 或使用poetry运行（推荐）
poetry run a_stock_analysis
```

### 使用示例

运行程序后，系统会自动执行以下流程：

1. 创建专业的A股分析师Agent
2. 分配市场分析和财务分析任务
3. Agent使用各种工具进行分析
4. 生成完整的股票分析报告

系统默认分析的是贵州茅台（600519.SH），您可以在`main.py`中修改分析目标。

## 项目结构

```
src/a_stock_analysis/
├── .env                # 环境变量配置文件
├── .env.example        # 环境变量模板文件
├── __init__.py         # 包初始化文件
├── crew.py             # CrewAI配置和Agent定义
├── main.py             # 主入口文件
├── config/             # 配置文件目录
│   ├── agents.yaml     # Agent配置
│   └── tasks.yaml      # Task配置
└── tools/              # 自定义工具集合
    ├── __init__.py     # 工具包初始化
    ├── a_stock_data_tool.py       # A股数据获取工具
    ├── financial_tool.py          # 财务分析工具
    ├── market_sentiment_tool.py   # 市场情绪分析工具
    └── calculator_tool.py         # 计算器工具
```

## 配置说明

### 环境变量配置

在`.env`文件中，您需要配置以下环境变量：

- `OPENAI_API_KEY`：OpenAI API密钥（用于LLM服务）
- 其他可能需要的API密钥（根据实际使用的服务）

### 配置文件

- `config/agents.yaml`：定义系统中使用的Agent及其角色、目标和背景
- `config/tasks.yaml`：定义Agent需要执行的任务

## 数据来源

本系统主要使用AKShare库获取A股市场数据：

- 实时行情数据：来自各大交易所的实时行情
- 历史数据：包含A股市场多年的交易数据
- 财务数据：上市公司公开披露的财务报表数据
- 板块数据：市场分类和板块行情信息

## 常见问题解答(FAQ)

### 1. 运行时出现`ImportError: cannot import name 'BaseTool'`错误怎么办？

这是因为crewAI版本更新导致API变更。请确保：
- 所有工具文件中使用`from crewai.tools import BaseTool`而非`from crewai import BaseTool`
- 使用正确版本的pydantic（v2.x）

### 2. 数据获取失败怎么办？

- 检查网络连接是否正常
- 确认AKShare库已正确安装且版本不低于1.12.0
- 验证股票代码格式是否正确（如：000001.SZ或600519.SH）

### 3. 如何修改分析的股票？

编辑`main.py`文件，修改`run()`函数中的股票代码参数。

### 4. 如何扩展系统功能？

- 在`tools`目录下创建新的工具文件
- 在`crew.py`中定义新的Agent或任务
- 在`config`目录下更新相关配置

## 贡献指南

我们欢迎社区贡献，如果您有任何想法或发现问题，请通过以下方式参与：

1. 提交Issue报告问题或提出新功能建议
2. 提交Pull Request贡献代码
3. 完善文档和示例

## 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。

## 免责声明

本系统仅提供数据分析服务，不构成任何投资建议。投资有风险，入市需谨慎。请在做出投资决策前进行充分的研究和分析。

## 致谢

- 感谢CrewAI团队提供强大的多Agent协作框架
- 感谢AKShare团队提供全面的A股市场数据接口
- 感谢所有为开源社区做出贡献的开发者