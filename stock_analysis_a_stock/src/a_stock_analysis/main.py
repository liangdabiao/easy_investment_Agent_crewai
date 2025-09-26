import sys
from crew import AStockAnalysisCrew

def run():
    """
    运行A股分析
    """
    inputs = {
        'company_name': '贵州茅台',
        'stock_code': '600519.SH',  # 港股腾讯，可改为A股代码如 '000001.SZ'
        'market': 'SH'  # HK=港股, SZ=深交所, SH=上交所
    }
    return AStockAnalysisCrew().crew().kickoff(inputs=inputs)

def train():
    """
    训练crew
    """
    inputs = {
        'company_name': '贵州茅台',
        'stock_code': '600519.SH',
        'market': 'SH'
    }
    try:
        AStockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)
    except Exception as e:
        raise Exception(f"训练crew时发生错误: {e}")

if __name__ == "__main__":
    print("## 欢迎使用A股智能分析系统")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## 分析报告")
    print("########################\n")
    print(result)