from tools.a_stock_data_tool import AStockDataTool

# 测试修复后的财务数据获取功能
try:
    print("=== 测试修复后的财务数据获取功能 ===")
    tool = AStockDataTool()
    
    # 测试贵州茅台(600519.SH)的财务数据
    print("\n获取贵州茅台(600519.SH)的财务数据：")
    financial_data = tool._run(stock_code="600519.SH", data_type="financial")
    print(financial_data)
    
    # 测试其他股票的财务数据
    print("\n获取万科A(000002.SZ)的财务数据：")
    financial_data_vanke = tool._run(stock_code="000002.SZ", data_type="financial")
    print(financial_data_vanke)
    
    # 测试板块数据功能（之前已修复）
    print("\n获取行业板块数据：")
    sector_data = tool._run(stock_code="", data_type="sector")
    print(sector_data[:500] + "...")  # 只打印部分内容
    
    print("\n=== 测试完成 ===")
except Exception as e:
    print(f"测试失败: {str(e)}")
    import traceback
    traceback.print_exc()