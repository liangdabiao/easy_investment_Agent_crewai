import akshare as ak

# 测试板块相关函数
try:
    print("=== 测试 stock_sector_spot ===")
    df_spot = ak.stock_sector_spot()
    print(f"数据形状: {df_spot.shape}")
    print("前5行数据:")
    print(df_spot.head())
    print("\n列名:", df_spot.columns.tolist())
except Exception as e:
    print(f"stock_sector_spot 测试失败: {e}")

try:
    print("\n=== 测试 stock_board_industry_index_ths ===")
    df_ths_industry = ak.stock_board_industry_index_ths()
    print(f"数据形状: {df_ths_industry.shape}")
    print("前5行数据:")
    print(df_ths_industry.head())
    print("\n列名:", df_ths_industry.columns.tolist())
except Exception as e:
    print(f"stock_board_industry_index_ths 测试失败: {e}")

try:
    print("\n=== 测试 stock_sector_rank_cxd_ths ===")  # 查看是否存在
    df_rank = ak.stock_rank_cxd_ths()
    print(f"数据形状: {df_rank.shape}")
    print("前5行数据:")
    print(df_rank.head())
    print("\n列名:", df_rank.columns.tolist())
except Exception as e:
    print(f"stock_sector_rank_cxd_ths 测试失败: {e}")