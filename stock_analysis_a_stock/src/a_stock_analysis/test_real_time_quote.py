#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试实时行情数据获取功能
"""

import akshare as ak
import pandas as pd


def test_stock_quote_functions():
    """测试AKShare中的实时行情函数"""
    print("开始测试实时行情数据获取功能...")
    print(f"当前AKShare版本: {ak.__version__}")
    
    # 测试主要的实时行情函数
    print("\n=== 测试stock_zh_a_spot函数 ===")
    try:
        df = ak.stock_zh_a_spot()
        print(f"返回数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        # 查看前几行数据
        print("前5行数据:")
        print(df.head())
        
        # 检查代码列的格式
        if '代码' in df.columns:
            print("\n代码列的一些示例值:")
            print(df['代码'].head(10).tolist())
            
            # 测试贵州茅台的代码格式
            maotai_code = "600519"
            print(f"\n查找贵州茅台代码 '{maotai_code}':")
            maotai_data = df[df['代码'] == maotai_code]
            if not maotai_data.empty:
                print(f"找到贵州茅台数据，行数: {len(maotai_data)}")
                print(maotai_data.iloc[0])
            else:
                print(f"未找到贵州茅台数据 '600519'")
                
                # 尝试其他可能的代码格式
                formats_to_try = ["sh600519", "SH600519", "600519.SH"]
                for fmt in formats_to_try:
                    print(f"\n尝试格式 '{fmt}':")
                    test_data = df[df['代码'] == fmt]
                    if not test_data.empty:
                        print(f"找到数据，行数: {len(test_data)}")
                        print(test_data.iloc[0])
                        break
                else:
                    print("所有尝试的代码格式都未找到数据")
    except Exception as e:
        print(f"stock_zh_a_spot函数调用失败: {str(e)}")
    
    # 测试备用的实时行情函数
    print("\n=== 测试备用函数 stock_zh_a_spot_em ===")
    try:
        df = ak.stock_zh_a_spot_em()
        print(f"返回数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        # 查找贵州茅台
        maotai_code = "600519"
        print(f"\n在stock_zh_a_spot_em中查找贵州茅台代码 '{maotai_code}':")
        maotai_data = df[df['代码'] == maotai_code]
        if not maotai_data.empty:
            print(f"找到贵州茅台数据，行数: {len(maotai_data)}")
            print(maotai_data.iloc[0])
        else:
            print(f"未找到贵州茅台数据 '{maotai_code}'")
    except Exception as e:
        print(f"stock_zh_a_spot_em函数调用失败: {str(e)}")
    
    # 测试其他可能的实时行情函数
    print("\n=== 测试其他实时行情函数 ===")
    try:
        # 测试新浪的实时行情接口
        print("\n测试stock_zh_a_spot_sina函数:")
        df = ak.stock_zh_a_spot_sina()
        print(f"返回数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        # 查找贵州茅台
        maotai_code = "sh600519"
        print(f"\n在stock_zh_a_spot_sina中查找贵州茅台代码 '{maotai_code}':")
        # 新浪的接口中，代码可能以不同的方式存储
        for col in df.columns:
            if col.lower() in ['code', '股票代码', '代码']:
                maotai_data = df[df[col] == maotai_code]
                if not maotai_data.empty:
                    print(f"找到贵州茅台数据，行数: {len(maotai_data)}")
                    print(maotai_data.iloc[0])
                    break
        else:
            print(f"未找到贵州茅台数据 '{maotai_code}'")
    except Exception as e:
        print(f"stock_zh_a_spot_sina函数调用失败: {str(e)}")


def main():
    """主函数"""
    test_stock_quote_functions()
    print("\n测试完成!")


if __name__ == "__main__":
    main()