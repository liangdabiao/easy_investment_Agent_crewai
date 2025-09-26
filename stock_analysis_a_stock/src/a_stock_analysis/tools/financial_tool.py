from crewai.tools import BaseTool
from typing import Any, Optional, Type
from pydantic import BaseModel, Field
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


class FinancialAnalysisToolSchema(BaseModel):
    """财务分析工具输入参数"""
    stock_code: str = Field(..., description="股票代码，如：000001.SZ或600519.SH")
    analysis_type: str = Field(..., description="分析类型：ratio（财务比率）、trend（趋势分析）、comparison（同业对比）")


class FinancialAnalysisTool(BaseTool):
    name: str = "财务分析工具"
    description: str = "深度分析A股公司财务报表，包括财务比率、趋势分析和同业对比"
    args_schema: Type[BaseModel] = FinancialAnalysisToolSchema

    def _run(self, stock_code: str, analysis_type: str = "ratio", **kwargs) -> Any:
        """执行财务分析"""
        try:
            if analysis_type == "ratio":
                return self._analyze_financial_ratios(stock_code)
            elif analysis_type == "trend":
                return self._analyze_financial_trend(stock_code)
            elif analysis_type == "comparison":
                return self._compare_industry_peers(stock_code)
            else:
                raise ValueError(f"不支持的分析类型: {analysis_type}")
        except Exception as e:
            return f"财务分析失败: {str(e)}"

    def _analyze_financial_ratios(self, stock_code: str) -> str:
        """分析财务比率"""
        try:
            # 确定市场类型
            if stock_code.endswith('.SZ'):
                market = "sz"
            elif stock_code.endswith('.SH'):
                market = "sh"
            else:
                return "无效的股票代码格式"

            code = stock_code.split('.')[0]

            # 获取财务指标
            df = ak.stock_financial_analysis_indicator(symbol=code)

            if df.empty:
                return f"未找到股票 {stock_code} 的财务数据"

            # 获取最新和去年同期数据
            latest = df.iloc[-1]
            last_year = df.iloc[-5] if len(df) >= 5 else df.iloc[0]

            result = f"""
股票 {stock_code} 财务比率分析：

=== 盈利能力分析 ===
• 每股收益：{latest['每股收益']:.3f}元
  同比变化：{((latest['每股收益'] - last_year['每股收益']) / abs(last_year['每股收益']) * 100):.2f}%

• 净资产收益率：{latest['净资产收益率']:.2f}%
  行业平均水平：15.0%
  评价：{'优秀' if latest['净资产收益率'] > 15 else '良好' if latest['净资产收益率'] > 10 else '一般'}

• 销售毛利率：{latest['销售毛利率']:.2f}%
  评价：{'很高' if latest['销售毛利率'] > 50 else '较高' if latest['销售毛利率'] > 30 else '一般'}

=== 偿债能力分析 ===
• 资产负债率：{latest['资产负债率']:.2f}%
  安全水平：{'很低' if latest['资产负债率'] < 30 else '适中' if latest['资产负债率'] < 60 else '较高'}

• 流动比率：{latest['流动比率']:.2f}
  偿债能力：{'很强' if latest['流动比率'] > 2 else '良好' if latest['流动比率'] > 1.5 else '一般'}

• 速动比率：{latest['速动比率']:.2f}
  短期偿债：{'优秀' if latest['速动比率'] > 1 else '良好' if latest['速动比率'] > 0.8 else '需关注'}

=== 成长能力分析 ===
• 营业收入同比增长：{latest['营业收入同比增长率']:.2f}%
  成长性：{'高增长' if latest['营业收入同比增长率'] > 20 else '稳健增长' if latest['营业收入同比增长率'] > 10 else '增速放缓'}

• 净利润同比增长：{latest['净利润同比增长率']:.2f}%
  盈利增长：{'强劲' if latest['净利润同比增长率'] > 30 else '良好' if latest['净利润同比增长率'] > 15 else '一般'}

=== 估值分析 ===
• 市盈率（动态）：{latest['市盈率-动态']:.2f}倍
  估值水平：{'低估' if latest['市盈率-动态'] < 15 else '合理' if latest['市盈率-动态'] < 30 else '高估'}

• 市净率：{latest['市净率']:.2f}倍
  估值评价：{'偏低' if latest['市净率'] < 1.5 else '合理' if latest['市净率'] < 3 else '偏高'}

=== 综合评分 ===
盈利能力：{'⭐⭐⭐⭐⭐' if latest['净资产收益率'] > 20 else '⭐⭐⭐⭐' if latest['净资产收益率'] > 15 else '⭐⭐⭐'}
偿债能力：{'⭐⭐⭐⭐⭐' if latest['流动比率'] > 2 and latest['资产负债率'] < 40 else '⭐⭐⭐⭐' if latest['流动比率'] > 1.5 else '⭐⭐⭐'}
成长能力：{'⭐⭐⭐⭐⭐' if latest['营业收入同比增长率'] > 30 else '⭐⭐⭐⭐' if latest['营业收入同比增长率'] > 15 else '⭐⭐⭐'}
估值水平：{'⭐⭐⭐⭐⭐' if latest['市盈率-动态'] < 15 else '⭐⭐⭐⭐' if latest['市盈率-动态'] < 25 else '⭐⭐⭐'}

"""
            return result

        except Exception as e:
            return f"财务比率分析失败: {str(e)}"

    def _analyze_financial_trend(self, stock_code: str) -> str:
        """分析财务趋势"""
        try:
            # 确定市场类型
            if stock_code.endswith('.SZ'):
                market = "sz"
            elif stock_code.endswith('.SH'):
                market = "sh"
            else:
                return "无效的股票代码格式"

            code = stock_code.split('.')[0]

            # 获取财务指标
            df = ak.stock_financial_analysis_indicator(symbol=code)

            if df.empty:
                return f"未找到股票 {stock_code} 的财务数据"

            # 获取最近8个季度的数据
            recent_data = df.tail(8)

            result = f"""
股票 {stock_code} 财务趋势分析（最近8个季度）：

{'季度':<15} {'每股收益':<10} {'净资产收益率':<12} {'营业收入增长':<12} {'净利润增长':<12}
{'-' * 75}
"""

            for i, (_, row) in enumerate(recent_data.iterrows()):
                result += f"Q{8-i:<13} {row['每股收益']:<10.3f} {row['净资产收益率']:<12.2f}% {row['营业收入同比增长率']:<12.2f}% {row['净利润同比增长率']:<12.2f}%\n"

            # 趋势分析
            eps_trend = recent_data['每股收益'].values
            roe_trend = recent_data['净资产收益率'].values

            result += "\n=== 趋势分析 ===\n"

            # EPS趋势
            eps_slope = (eps_trend[-1] - eps_trend[0]) / len(eps_trend) if len(eps_trend) > 1 else 0
            result += f"每股收益趋势：{'↗️ 持续增长' if eps_slope > 0.05 else '→ 保持稳定' if abs(eps_slope) <= 0.05 else '↘️ 有所下降'}\n"

            # ROE趋势
            roe_slope = (roe_trend[-1] - roe_trend[0]) / len(roe_trend) if len(roe_trend) > 1 else 0
            result += f"净资产收益率趋势：{'↗️ 持续改善' if roe_slope > 1 else '→ 保持稳定' if abs(roe_slope) <= 1 else '↘️ 有所下滑'}\n"

            # 波动性分析
            eps_volatility = eps_trend.std() / eps_trend.mean() if eps_trend.mean() > 0 else 0
            result += f"业绩稳定性：{'非常稳定' if eps_volatility < 0.1 else '相对稳定' if eps_volatility < 0.2 else '波动较大'}\n"

            return result

        except Exception as e:
            return f"财务趋势分析失败: {str(e)}"

    def _compare_industry_peers(self, stock_code: str) -> str:
        """同业对比分析"""
        try:
            # 确定市场类型
            if stock_code.endswith('.SZ'):
                market = "sz"
            elif stock_code.endswith('.SH'):
                market = "sh"
            else:
                return "无效的股票代码格式"

            code = stock_code.split('.')[0]

            # 获取目标公司数据
            target_df = ak.stock_financial_analysis_indicator(symbol=code)
            if target_df.empty:
                return f"未找到股票 {stock_code} 的财务数据"

            target_latest = target_df.iloc[-1]

            # 简化的同业对比（基于行业平均数据）
            # 注意：实际应用中需要获取真实的同行业公司数据进行对比
            industry_avg_roe = 12.5
            industry_avg_pe = 18.0
            industry_avg_pb = 2.1
            industry_avg_debt_ratio = 45.0

            result = f"""
股票 {stock_code} 同业对比分析：

=== 核心指标对比 ===
指标             本公司         行业平均         差异           评价
------------------------------------------------------------------------------
净资产收益率     {target_latest['净资产收益率']:.2f}%      {industry_avg_roe:.2f}%      {target_latest['净资产收益率'] - industry_avg_roe:+.2f}%      {'领先' if target_latest['净资产收益率'] > industry_avg_roe else '落后'}
市盈率           {target_latest['市盈率-动态']:.2f}倍       {industry_avg_pe:.2f}倍       {target_latest['市盈率-动态'] - industry_avg_pe:+.2f}倍      {'相对低估' if target_latest['市盈率-动态'] < industry_avg_pe else '相对高估'}
市净率           {target_latest['市净率']:.2f}倍        {industry_avg_pb:.2f}倍        {target_latest['市净率'] - industry_avg_pb:+.2f}倍      {'相对低估' if target_latest['市净率'] < industry_avg_pb else '相对高估'}
资产负债率       {target_latest['资产负债率']:.2f}%      {industry_avg_debt_ratio:.2f}%      {target_latest['资产负债率'] - industry_avg_debt_ratio:+.2f}%      {'较低' if target_latest['资产负债率'] < industry_avg_debt_ratio else '较高'}

=== 竞争力评估 ===
"""

            # 综合竞争力评分
            roe_score = min(max((target_latest['净资产收益率'] - industry_avg_roe) / industry_avg_roe * 10, -5), 5)
            pe_score = min(max((industry_avg_pe - target_latest['市盈率-动态']) / industry_avg_pe * 10, -5), 5)
            debt_score = min(max((industry_avg_debt_ratio - target_latest['资产负债率']) / industry_avg_debt_ratio * 10, -5), 5)

            total_score = roe_score + pe_score + debt_score

            result += f"盈利能力得分：{roe_score:+.1f} 分\n"
            result += f"估值吸引力得分：{pe_score:+.1f} 分\n"
            result += f"财务健康得分：{debt_score:+.1f} 分\n"
            result += f"综合得分：{total_score:+.1f} 分\n\n"

            if total_score > 5:
                result += "🏆 综合评价：公司具有较强的行业竞争力"
            elif total_score > 0:
                result += "👍 综合评价：公司具有一定竞争优势"
            elif total_score > -5:
                result += "📊 综合评价：公司竞争力一般"
            else:
                result += "⚠️ 综合评价：公司竞争力相对较弱"

            return result

        except Exception as e:
            return f"同业对比分析失败: {str(e)}"