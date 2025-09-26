#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的财务数据和板块数据获取功能
"""

import sys
import os
import pandas as pd
import akshare as ak

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入AStockDataTool类
try:
    from tools.a_stock_data_tool import AStockDataTool
    print("成功导入AStockDataTool类")
except Exception as e:
    print(f"导入AStockDataTool类失败: {str(e)}")
    sys.exit(1)


def test_financial_data():
    """测试财务数据获取功能"""
    print("\n=== 测试财务数据获取功能 ===")
    tool = AStockDataTool()
    
    # 测试贵州茅台(600519.SH)
    print("\n测试贵州茅台(600519.SH):")
    result = tool._get_financial_data("600519.SH")
    print(result)
    
    # 测试万科A(000002.SZ)
    print("\n测试万科A(000002.SZ):")
    result = tool._get_financial_data("000002.SZ")
    print(result)


def test_sector_data():
    """测试行业板块数据获取功能"""
    print("\n=== 测试行业板块数据获取功能 ===")
    tool = AStockDataTool()
    
    result = tool._get_sector_data()
    print(result)


def test_akshare_functions():
    """直接测试AKShare的相关函数"""
    print("\n=== 直接测试AKShare的相关函数 ===")
    
    # 测试财务数据函数
    print("\n测试stock_financial_analysis_indicator函数:")
    try:
        df = ak.stock_financial_analysis_indicator(symbol="600519")
        print(f"返回数据形状: {df.shape}")
        if not df.empty:
            print(f"列名: {list(df.columns)}")
            print("前3行数据:")
            print(df.head(3))
    except Exception as e:
        print(f"函数调用失败: {str(e)}")
    
    # 测试备用财务数据函数
    print("\n测试stock_financial_abstract_ths函数:")
    try:
        df = ak.stock_financial_abstract_ths(symbol="600519")
        print(f"返回数据形状: {df.shape}")
        if not df.empty:
            print(f"列名: {list(df.columns)}")
            print("前3行数据:")
            print(df.head(3))
    except Exception as e:
        print(f"函数调用失败: {str(e)}")
    
    # 测试板块数据函数
    print("\n测试stock_sector_spot函数:")
    try:
        df = ak.stock_sector_spot()
        print(f"返回数据形状: {df.shape}")
        if not df.empty:
            print(f"列名: {list(df.columns)}")
            print("前3行数据:")
            print(df.head(3))
    except Exception as e:
        print(f"函数调用失败: {str(e)}")
    
    # 测试备用板块数据函数
    print("\n测试stock_board_industry_name_ths函数:")
    try:
        df = ak.stock_board_industry_name_ths()
        print(f"返回类型: {type(df)}")
        if isinstance(df, pd.DataFrame):
            print(f"数据形状: {df.shape}")
            if not df.empty:
                print(f"列名: {list(df.columns)}")
                print("前3行数据:")
                print(df.head(3))
        elif isinstance(df, list):
            print(f"列表长度: {len(df)}")
            print(f"前5个元素: {df[:5]}")
    except Exception as e:
        print(f"函数调用失败: {str(e)}")


def main():
    """主函数"""
    print("开始测试修复后的A股数据获取功能...")
    print(f"当前AKShare版本: {ak.__version__}")
    
    # 测试财务数据获取
    test_financial_data()
    
    # 测试行业板块数据获取
    test_sector_data()
    
    # 直接测试AKShare函数
    test_akshare_functions()
    
    print("\n测试完成!")


if __name__ == "__main__":
    main()