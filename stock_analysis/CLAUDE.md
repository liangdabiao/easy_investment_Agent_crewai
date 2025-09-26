# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrewAI-based stock analysis project that orchestrates multiple AI agents to perform comprehensive financial analysis of stocks. The project creates a collaborative workflow between specialized agents (financial analyst, research analyst, investment advisor) to analyze stocks using various tools including SEC filings, web scraping, and financial calculations.

## Development Environment

### Dependencies
- Python 3.12+ (up to 3.13)
- Uses Poetry for dependency management (`pyproject.toml`)
- Main dependencies: `crewai[tools]>=0.152.0`, `python-dotenv`, `html2text`, `sec-api`
- Currently configured to use Ollama with `llama3.1` model (can be switched to OpenAI GPT models)

### Required Environment Variables
Create a `.env` file based on `.env.example` with:
- `SEC_API_API_KEY` - for SEC filings API access
- OpenAI API key (if using GPT models instead of Ollama)

### Commands
- **Install dependencies**: `poetry install --no-root`
- **Run main analysis**: `poetry run python3 main.py` (from project root)
- **Run training**: `poetry run python3 src/stock_analysis/main.py` with iteration count
- **Use installed script**: `poetry run stock_analysis`

## Architecture

### Core Components

**src/stock_analysis/main.py**: Entry point that executes the crew with default inputs (currently hardcoded to analyze 'AMZN'). Contains `run()` for analysis and `train()` for crew training.

**src/stock_analysis/crew.py**: Main orchestration file using CrewAI's `@CrewBase` decorator. Defines:
- Three specialized agents with different roles and tools
- Four sequential tasks that work together
- Uses YAML configuration files for agent and task definitions

**src/stock_analysis/tools/**: Custom tools for agents:
- `calculator_tool.py`: Safe mathematical expression evaluator using AST parsing
- `sec_tools.py`: SEC filing analysis tools (10-K and 10-Q) that fetch and search SEC documents

### Configuration Files

**src/stock_analysis/config/agents.yaml**: Defines three agent roles:
- `financial_analyst`: Financial data and market trends expert
- `research_analyst`: News and market sentiment specialist
- `investment_advisor`: Strategic investment recommendation expert

**src/stock_analysis/config/tasks.yaml**: Defines four sequential tasks:
- `financial_analysis`: Financial metrics and performance analysis
- `research`: News and market sentiment gathering
- `filings_analysis`: SEC EDGAR filings analysis
- `recommend`: Final investment recommendation synthesis

### Agent Workflow

The crew operates sequentially:
1. **Research Analysis** → **Financial Analysis** → **Filings Analysis** → **Investment Recommendation**
2. Each agent has access to specific tools:
   - All agents can scrape websites and search
   - Financial agent gets calculator tool
   - Financial/Research agents get SEC filing tools
   - Investment advisor synthesizes all previous analysis

### Key Implementation Details

- Uses Ollama's `llama3.1` model by default (line 13-14 in crew.py)
- SEC tools use `sec-api` for fetching 10-K/10-Q filings and embedchain for semantic search
- Calculator tool implements safe expression evaluation using AST parsing
- Agents are configured with verbose logging for debugging
- The workflow is sequential but could be modified for parallel processing

## Common Modifications

- **Change target stock**: Update `company_stock` in main.py (currently 'AMZN')
- **Switch LLM**: Replace Ollama initialization with OpenAI ChatOpenAI in crew.py
- **Add new tools**: Create new tool classes extending BaseTool
- **Modify agent roles**: Edit agents.yaml or crew.py tool assignments
- **Change task flow**: Modify task definitions in tasks.yaml or crew process order