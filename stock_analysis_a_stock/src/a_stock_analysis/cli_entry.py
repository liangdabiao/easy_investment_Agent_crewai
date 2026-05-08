#!/usr/bin/env python3
"""
CLI entry point for A股分析系统
用于PyInstaller打包和命令行调用
"""
import sys
import os
import argparse
from crew import AStockAnalysisCrew

def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(description='A股智能分析系统')
    parser.add_argument('--company', type=str, required=True, help='公司名称')
    parser.add_argument('--code', type=str, required=True, help='股票代码')
    parser.add_argument('--market', type=str, required=True, help='市场类型 (SH/SZ/HK)')
    
    args = parser.parse_args()
    
    inputs = {
        'company_name': args.company,
        'stock_code': args.code,
        'market': args.market
    }
    
    print("## 欢迎使用A股智能分析系统")
    print('-------------------------------')
    print(f"正在分析: {inputs['company_name']} ({inputs['stock_code']})")
    print('-------------------------------')
    
    try:
        result = AStockAnalysisCrew().crew().kickoff(inputs=inputs)
        
        print("\n\n########################")
        print("## 分析报告")
        print("########################\n")
        print(result)
        
        return 0
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
