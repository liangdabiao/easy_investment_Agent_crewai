#!/bin/bash
# Quick start script for A股智能分析系统 UI

echo "=================================="
echo "A股智能分析系统 UI"
echo "=================================="
echo ""

# Check if binary exists
if [ ! -f "stock-analysis-ui-linux-amd64" ]; then
    echo "可执行文件不存在，正在编译..."
    go build -o stock-analysis-ui-linux-amd64 main.go
    if [ $? -ne 0 ]; then
        echo "编译失败！请检查Go环境和依赖。"
        exit 1
    fi
    echo "编译成功！"
    echo ""
fi

echo "启动UI服务器..."
echo "访问地址: http://localhost:8080"
echo "按 Ctrl+C 停止服务器"
echo ""

./stock-analysis-ui-linux-amd64
