from crewai.tools import BaseTool
from typing import Any, Optional, Type
from pydantic import BaseModel, Field
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


class AStockDataToolSchema(BaseModel):
    """A股数据工具输入参数"""
    stock_code: str = Field(..., description="股票代码，如：000001.SZ（深交所）或600519.SH（上交所）")
    data_type: str = Field(..., description="数据类型：quote（实时行情）、daily（日线数据）、financial（财务数据）、sector（板块数据）")


class AStockDataTool(BaseTool):
    name: str = "A股数据获取工具"
    description: str = "获取A股股票的实时行情、历史数据、财务信息等，支持上交所和深交所股票"
    args_schema: Type[BaseModel] = AStockDataToolSchema

    def _run(self, stock_code: str, data_type: str = "quote", **kwargs) -> Any:
        """获取A股数据"""
        try:
            if data_type == "quote":
                return self._get_real_time_quote(stock_code)
            elif data_type == "daily":
                return self._get_daily_data(stock_code)
            elif data_type == "financial":
                return self._get_financial_data(stock_code)
            elif data_type == "sector":
                return self._get_sector_data()
            else:
                raise ValueError(f"不支持的数据类型: {data_type}")
        except Exception as e:
            return f"获取数据时发生错误: {str(e)}"

    def _get_real_time_quote(self, stock_code: str) -> str:
        """获取实时行情数据"""
        try:
            # 提取股票代码部分，处理不同格式
            if stock_code.endswith('.SZ') or stock_code.endswith('.SH'):
                code = stock_code.split('.')[0]
            elif len(stock_code) > 2 and (stock_code[:2] == 'sz' or stock_code[:2] == 'sh' or 
                                         stock_code[:2] == 'SZ' or stock_code[:2] == 'SH'):
                # 处理sh600519或sz000001格式
                code = stock_code[2:]
            else:
                # 直接使用传入的代码
                code = stock_code

            # 获取实时行情数据，尝试多个数据源
            # 1. 首先尝试主数据源
            try:
                df = ak.stock_zh_a_spot()
                # 尝试精确匹配代码
                stock_data = df[df['代码'] == code]
                
                # 如果主数据源失败，尝试备用数据源
                if stock_data.empty:
                    df = ak.stock_zh_a_spot_em()
                    stock_data = df[df['代码'] == code]
            except Exception as e:
                # 如果主数据源出错，直接尝试备用数据源
                df = ak.stock_zh_a_spot_em()
                stock_data = df[df['代码'] == code]

            if stock_data.empty:
                # 提供更详细的错误信息
                return f"未找到股票 {stock_code} 的实时数据。请检查代码格式或尝试使用其他数据源。"

            # 提取主要信息
            row = stock_data.iloc[0]
            
            # 安全地构建结果字符串，检查每个字段是否存在
            result = f"股票：{row.get('名称', '未知')} ({stock_code})\n"
            
            if '最新价' in row:
                try:
                    result += f"当前价格：{float(row['最新价']):.2f}\n"
                except (ValueError, TypeError):
                    result += f"当前价格：{row['最新价']}\n"
            
            if '涨跌幅' in row:
                try:
                    result += f"涨跌幅：{float(row['涨跌幅']):.2f}%\n"
                except (ValueError, TypeError):
                    result += f"涨跌幅：{row['涨跌幅']}\n"
            
            if '涨跌额' in row:
                try:
                    result += f"涨跌额：{float(row['涨跌额']):.2f}\n"
                except (ValueError, TypeError):
                    result += f"涨跌额：{row['涨跌额']}\n"
            
            if '成交量' in row:
                try:
                    result += f"成交量：{int(row['成交量']):,}\n"
                except (ValueError, TypeError):
                    result += f"成交量：{row['成交量']}\n"
            
            if '成交额' in row:
                try:
                    result += f"成交额：{int(row['成交额']):,}\n"
                except (ValueError, TypeError):
                    result += f"成交额：{row['成交额']}\n"
            
            # 添加其他重要字段
            important_fields = ['最高', '最低', '今开', '昨收', '市盈率-动态', '市净率', '总市值', '流通市值']
            field_names = {'最高': '最高价', '最低': '最低价', '今开': '开盘价', '昨收': '昨收价',
                          '市盈率-动态': '市盈率', '市净率': '市净率', '总市值': '总市值', '流通市值': '流通市值'}
            
            for field in important_fields:
                if field in row:
                    try:
                        if field in ['最高', '最低', '今开', '昨收']:
                            result += f"{field_names[field]}：{float(row[field]):.2f}\n"
                        elif field in ['市盈率-动态', '市净率']:
                            result += f"{field_names[field]}：{float(row[field]):.2f}\n"
                        elif field in ['总市值', '流通市值']:
                            result += f"{field_names[field]}：{int(row[field]):,}\n"
                    except (ValueError, TypeError):
                        result += f"{field_names[field]}：{row[field]}\n"

            return result

        except Exception as e:
            return f"获取实时行情失败: {str(e)}"

    def _get_daily_data(self, stock_code: str, period: str = "daily") -> str:
        """获取历史K线数据"""
        try:
            # 确定市场类型
            if stock_code.endswith('.SZ'):
                market = "sz"
            elif stock_code.endswith('.SH'):
                market = "sh"
            else:
                return "无效的股票代码格式"

            code = stock_code.split('.')[0]

            # 获取历史数据（最近30天）
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

            df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                   start_date=start_date, end_date=end_date,
                                   adjust="qfq")

            if df.empty:
                return f"未找到股票 {stock_code} 的历史数据"

            # 计算技术指标
            df['MA5'] = df['收盘'].rolling(window=5).mean()
            df['MA10'] = df['收盘'].rolling(window=10).mean()
            df['MA20'] = df['收盘'].rolling(window=20).mean()

            # 获取最近的数据
            recent_data = df.tail(10)

            result = f"""
股票 {stock_code} 最近10个交易日数据：
{'日期':<12} {'开盘':<8} {'最高':<8} {'最低':<8} {'收盘':<8} {'涨跌幅':<8} {'成交量':<12}
{'-'*80}
"""

            for _, row in recent_data.iterrows():
                result += f"{row['日期']:<12} {row['开盘']:<8.2f} {row['最高']:<8.2f} {row['最低']:<8.2f} {row['收盘']:<8.2f} {row['涨跌幅']:<8.2f}% {row['成交量']:<12,}\n"

            # 技术分析
            latest = df.iloc[-1]
            prev_ma5 = df.iloc[-6]['MA5'] if len(df) > 5 else None
            current_ma5 = df.iloc[-1]['MA5']

            result += f"\n技术分析：\n"
            result += f"当前价格：{latest['收盘']:.2f}\n"
            result += f"MA5：{current_ma5:.2f}\n"
            result += f"MA10：{df.iloc[-1]['MA10']:.2f}\n"
            result += f"MA20：{df.iloc[-1]['MA20']:.2f}\n"

            if prev_ma5 and current_ma5:
                if latest['收盘'] > current_ma5 > prev_ma5:
                    result += "趋势：短期上升趋势\n"
                elif latest['收盘'] < current_ma5 < prev_ma5:
                    result += "趋势：短期下降趋势\n"
                else:
                    result += "趋势：震荡整理\n"

            return result

        except Exception as e:
            return f"获取历史数据失败: {str(e)}"

    def _get_financial_data(self, stock_code: str) -> str:
        """获取财务数据"""
        try:
            # 确定市场类型
            if stock_code.endswith('.SZ'):
                market = "sz"
            elif stock_code.endswith('.SH'):
                market = "sh"
            else:
                return "无效的股票代码格式"

            code = stock_code.split('.')[0]

            # 获取主要财务指标
            try:
                df = ak.stock_financial_analysis_indicator(symbol=code)
            except Exception as e:
                return f"获取财务数据失败: {str(e)}"

            if df.empty:
                # 如果第一个函数失败，尝试使用同花顺的财务摘要数据
                try:
                    df = ak.stock_financial_abstract_ths(symbol=code)
                    if df.empty:
                        return f"未找到股票 {stock_code} 的财务数据"
                except Exception as e:
                    return f"未找到股票 {stock_code} 的财务数据: {str(e)}"

            # 获取最新的财务数据
            latest_data = df.iloc[-1]

            # 构建结果字符串，根据可用字段动态调整
            result = f"股票 {stock_code} 主要财务指标：\n\n"
            result += "盈利能力：\n"
            
            # 检查并添加可用的字段，添加严格的类型转换和错误处理
            if '每股收益' in df.columns and pd.notna(latest_data['每股收益']):
                try:
                    eps_value = float(latest_data['每股收益'])
                    result += f"  每股收益：{eps_value:.3f}元\n"
                except (ValueError, TypeError):
                    result += f"  每股收益：{latest_data['每股收益']}\n"
            
            if '净资产收益率' in df.columns and pd.notna(latest_data['净资产收益率']):
                try:
                    roe_value = float(latest_data['净资产收益率'])
                    result += f"  净资产收益率：{roe_value:.2f}%\n"
                except (ValueError, TypeError):
                    result += f"  净资产收益率：{latest_data['净资产收益率']}\n"
            elif '净资产收益率-摊薄' in df.columns and pd.notna(latest_data['净资产收益率-摊薄']):
                try:
                    roe_value = float(latest_data['净资产收益率-摊薄'])
                    result += f"  净资产收益率：{roe_value:.2f}%\n"
                except (ValueError, TypeError):
                    result += f"  净资产收益率：{latest_data['净资产收益率-摊薄']}\n"
            
            if '销售毛利率' in df.columns and pd.notna(latest_data['销售毛利率']):
                try:
                    gross_margin = float(latest_data['销售毛利率'])
                    result += f"  销售毛利率：{gross_margin:.2f}%\n"
                except (ValueError, TypeError):
                    result += f"  销售毛利率：{latest_data['销售毛利率']}\n"
            
            result += "\n偿债能力：\n"
            if '资产负债率' in df.columns and pd.notna(latest_data['资产负债率']):
                try:
                    # 确保资产负债率是数值
                    if isinstance(latest_data['资产负债率'], str):
                        # 去除百分号并转换为浮点数
                        debt_ratio = float(latest_data['资产负债率'].replace('%', '').strip())
                    else:
                        debt_ratio = float(latest_data['资产负债率'])
                    result += f"  资产负债率：{debt_ratio:.2f}%\n"
                except (ValueError, TypeError):
                    result += f"  资产负债率：{latest_data['资产负债率']}\n"
            
            if '流动比率' in df.columns and pd.notna(latest_data['流动比率']):
                try:
                    current_ratio = float(latest_data['流动比率'])
                    result += f"  流动比率：{current_ratio:.2f}\n"
                except (ValueError, TypeError):
                    result += f"  流动比率：{latest_data['流动比率']}\n"
            
            if '速动比率' in df.columns and pd.notna(latest_data['速动比率']):
                try:
                    quick_ratio = float(latest_data['速动比率'])
                    result += f"  速动比率：{quick_ratio:.2f}\n"
                except (ValueError, TypeError):
                    result += f"  速动比率：{latest_data['速动比率']}\n"
            
            result += "\n成长能力：\n"
            if '净利润同比增长率' in df.columns and pd.notna(latest_data['净利润同比增长率']):
                try:
                    # 处理不同格式的增长率
                    if isinstance(latest_data['净利润同比增长率'], str):
                        if '%' in latest_data['净利润同比增长率']:
                            growth_rate = float(latest_data['净利润同比增长率'].replace('%', '').strip())
                        else:
                            growth_rate = float(latest_data['净利润同比增长率'])
                    else:
                        growth_rate = float(latest_data['净利润同比增长率'])
                    result += f"  净利润同比增长：{growth_rate:.2f}%\n"
                except (ValueError, TypeError):
                    result += f"  净利润同比增长：{latest_data['净利润同比增长率']}\n"
            
            # 添加报告期信息
            if '报告期' in df.columns:
                result += f"\n报告期：{latest_data['报告期']}\n"

            return result

        except Exception as e:
            return f"获取财务数据失败: {str(e)}"

    def _get_sector_data(self) -> str:
        """获取行业板块数据"""
        try:
            # 获取行业板块数据，并添加异常处理
            try:
                df = ak.stock_sector_spot()
            except Exception as e:
                # 尝试使用备用函数获取板块数据
                try:
                    df = ak.stock_board_industry_name_ths()
                    # 如果获取到的是板块名称列表而不是数据框，进行特殊处理
                    if isinstance(df, list):
                        result = "行业板块列表：\n\n"
                        for i, sector in enumerate(df[:10]):
                            result += f"{i+1}. {sector}\n"
                        return result
                    elif not df.empty:
                        # 基本数据处理
                        result = "行业板块列表：\n\n"
                        for i, row in df.iterrows():
                            if i >= 10:  # 限制显示前10个
                                break
                            # 尝试获取板块名称，处理不同的数据结构
                            sector_name = row.get('板块名称') or row.get('行业名称') or row.get(0) or str(row)
                            result += f"{i+1}. {sector_name}\n"
                        return result
                except:
                    # 如果备用函数也失败，返回通用错误信息
                    return f"获取行业板块数据失败: {str(e)}"
            
            if df.empty:
                return "暂无行业板块数据"
            
            # 按涨跌幅排序，取前10个板块（仅当涨跌幅列存在时）
            if '涨跌幅' in df.columns:
                df = df.sort_values(by='涨跌幅', ascending=False).head(10)
            else:
                # 如果没有涨跌幅列，取前10个板块
                df = df.head(10)
            
            # 调整列名以匹配模板
            if '名称' in df.columns and '板块' not in df.columns:
                df = df.rename(columns={'名称': '板块'})
            if '领涨股' in df.columns and '股票名称' not in df.columns:
                df = df.rename(columns={'领涨股': '股票名称'})
            
            # 构建结果字符串
            result = "行业板块涨跌幅排行（前10）：\n\n"
            for idx, row in df.iterrows():
                # 安全地获取涨跌幅和领涨股信息
                sector_name = row.get('板块') or str(row.get(0) or row.get('行业名称') or '未知板块')
                
                # 处理涨跌幅信息
                if '涨跌幅' in row:
                    try:
                        change_rate = float(row['涨跌幅'])
                        change_text = f"{change_rate:.2f}%"
                    except (ValueError, TypeError):
                        change_text = str(row['涨跌幅'])
                else:
                    change_text = "--"
                
                # 处理领涨股信息
                if '股票名称' in row:
                    leading_stock = str(row['股票名称'])
                elif '领涨股' in row:
                    leading_stock = str(row['领涨股'])
                else:
                    leading_stock = "--"
                
                result += f"{idx+1}. {sector_name}: {change_text} - 领涨股: {leading_stock}\n"
            
            return result
            
        except Exception as e:
            return f"获取行业板块数据失败: {str(e)}"