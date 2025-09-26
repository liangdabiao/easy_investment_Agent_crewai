import akshare as ak
import pandas as pd
import traceback

# 定义要测试的股票代码
symbol = "600519"

# 测试单个财务函数的辅助函数
def test_financial_function(func_name, **kwargs):
    print(f"\n=== 测试 {func_name} 函数 ===")
    try:
        if hasattr(ak, func_name):
            func = getattr(ak, func_name)
            result = func(**kwargs)
            print(f"函数调用成功")
            if isinstance(result, pd.DataFrame):
                print(f"数据形状: {result.shape}")
                if not result.empty:
                    print(f"列名: {result.columns.tolist()}")
                    print(f"数据预览:\n{result.head(2)}")
                else:
                    print("返回的数据框为空")
            else:
                print(f"返回类型: {type(result)}")
                print(f"返回值预览: {str(result)[:500]}")
            return result
        else:
            print(f"函数 {func_name} 不存在")
            return None
    except Exception as e:
        print(f"函数调用失败: {str(e)}")
        print("错误堆栈:")
        traceback.print_exc()
        return None

# 测试多个财务函数
if __name__ == "__main__":
    print(f"测试股票代码: {symbol}")
    print(f"AKShare版本: {ak.__version__}")
    
    # 尝试不同的财务数据函数
    test_financial_function("stock_financial_analysis_indicator", symbol=symbol)
    
    # 测试eastmoney的财务指标
    test_financial_function("stock_financial_analysis_indicator_em", symbol=symbol)
    
    # 测试新浪的财务数据
    test_financial_function("stock_financial_report_sina", symbol=f"sh{symbol}")
    
    # 测试财务摘要
    test_financial_function("stock_financial_abstract", symbol=symbol)
    
    # 测试同花顺的财务数据
    test_financial_function("stock_financial_abstract_ths", symbol=symbol)
    
    # 尝试获取财务报表数据
    test_financial_function("stock_financial_report_sina", symbol=f"sh{symbol}")
    
    # 尝试不同的股票代码格式
    print("\n=== 测试不同的股票代码格式 ===")
    code_formats = [symbol, f"sh{symbol}", f"{symbol}.SH"]
    for code in code_formats:
        print(f"\n测试代码格式: {code}")
        # 尝试最基础的函数
        try:
            df = ak.stock_zh_a_spot()
            stock_data = df[df['代码'] == code.split('.')[0]]
            if not stock_data.empty:
                print(f"找到股票数据: {stock_data['名称'].values[0]}")
            else:
                print("未找到股票数据")
        except Exception as e:
            print(f"查找股票数据失败: {e}")
    
    # 尝试获取实时行情，确认股票代码有效性
    print("\n=== 测试实时行情函数 ===")
    try:
        df_spot = ak.stock_zh_a_spot()
        maotai_data = df_spot[df_spot['代码'] == symbol]
        if not maotai_data.empty:
            print(f"茅台股票信息: {maotai_data.iloc[0]['名称']} ({maotai_data.iloc[0]['代码']})")
            print(f"当前价格: {maotai_data.iloc[0]['最新价']}")
        else:
            print("未找到茅台股票数据")
    except Exception as e:
        print(f"获取实时行情失败: {e}")