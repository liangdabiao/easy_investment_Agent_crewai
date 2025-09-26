#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的实时行情数据获取功能
"""
import sys
import os
from tools.a_stock_data_tool import AStockDataTool

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_real_time_quote():
    """测试修复后的实时行情获取功能"""
    print("=== 测试实时行情数据获取功能 ===")
    
    # 初始化工具
    tool = AStockDataTool()
    
    # 测试不同格式的股票代码
    stock_codes = [
        "600519.SH",  # 贵州茅台，带后缀
        "sh600519",   # 贵州茅台，带前缀
        "600519",     # 贵州茅台，纯数字代码
        "000002.SZ",  # 万科A，带后缀
        "sz000002",   # 万科A，带前缀
        "000002"      # 万科A，纯数字代码
    ]
    
    for stock_code in stock_codes:
        try:
            print(f"\n获取股票 {stock_code} 的实时数据：")
            # 使用正确的方法调用方式
            result = tool._run(stock_code=stock_code, data_type="quote")
            print(result)
        except Exception as e:
            print(f"获取 {stock_code} 实时数据失败：{str(e)}")


if __name__ == "__main__":
    test_real_time_quote()