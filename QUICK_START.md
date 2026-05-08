# 快速开始指南 - A股智能分析系统

本指南帮助您在5分钟内启动并使用UI界面进行股票分析。

## 🚀 一站式启动（推荐）

### Windows用户

1. **确保已安装Python 3.12+**
   ```bash
   python --version
   ```

2. **配置Python环境（首次运行）**
   ```bash
   cd stock_analysis_a_stock
   poetry install --no-root
   # 或使用 uv sync
   ```

3. **启动UI界面**
   ```bash
   cd ui
   run.bat
   ```
   
   浏览器会自动打开，开始使用！

### Linux/macOS用户

1. **确保已安装Python 3.12+**
   ```bash
   python3 --version
   ```

2. **配置Python环境（首次运行）**
   ```bash
   cd stock_analysis_a_stock
   poetry install --no-root
   # 或使用 uv sync
   ```

3. **启动UI界面**
   ```bash
   cd ui
   chmod +x run.sh
   ./run.sh
   ```
   
   浏览器会自动打开，开始使用！

## 📖 使用UI界面

1. **打开界面**
   - 浏览器自动打开 http://localhost:8080
   - 如果没有自动打开，手动访问该地址

2. **选择股票**
   - 方式A：点击示例股票（贵州茅台、平安银行、腾讯控股）
   - 方式B：手动输入公司名称、股票代码和市场类型

3. **开始分析**
   - 点击"🚀 开始分析"按钮
   - 实时查看分析进度和输出
   - 等待分析完成

4. **查看结果**
   - 完整的分析报告会显示在页面下方
   - 可以复制保存结果

## 🎯 示例股票

### 贵州茅台（上交所）
```
公司名称: 贵州茅台
股票代码: 600519.SH
市场类型: 上交所(SH)
```

### 平安银行（深交所）
```
公司名称: 平安银行
股票代码: 000001.SZ
市场类型: 深交所(SZ)
```

### 腾讯控股（港股）
```
公司名称: 腾讯控股
股票代码: 00700.HK
市场类型: 港股(HK)
```

## 🛠️ 传统命令行方式

如果您更喜欢命令行界面：

```bash
cd stock_analysis_a_stock
poetry run python src/a_stock_analysis/main.py
```

## ❓ 常见问题

### Q: 提示"未找到Python环境"？
**A:** 确保Python已安装并在系统PATH中：
```bash
# Windows
python --version

# Linux/macOS
python3 --version
```

### Q: 分析时出错？
**A:** 检查以下几点：
1. Python依赖是否完整安装
2. 股票代码格式是否正确
3. `.env` 文件是否正确配置

### Q: 端口被占用？
**A:** 更改端口：
```bash
# Windows
set PORT=9090
run.bat

# Linux/macOS
export PORT=9090
./run.sh
```

### Q: 想编译自己的可执行文件？
**A:** 使用build脚本：
```bash
# Windows
cd ui
build.bat

# Linux/macOS
cd ui
chmod +x build.sh
./build.sh
```

## 📚 更多文档

- **详细UI使用指南**: [UI_使用指南.md](./UI_使用指南.md)
- **技术文档**: [ui/README.md](./ui/README.md)
- **项目总览**: [README.md](./README.md)

## 🎉 开始分析

一切准备就绪！现在运行 `cd ui && run.bat`（Windows）或 `cd ui && ./run.sh`（Linux/macOS）开始您的股票分析之旅！

---

**免责声明**: 本系统提供的分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。
