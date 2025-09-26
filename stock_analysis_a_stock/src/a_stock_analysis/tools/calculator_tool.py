from crewai.tools import BaseTool
import ast
import operator
import re


class CalculatorTool(BaseTool):
    name: str = "计算器工具"
    description: str = (
        "用于执行各种数学计算，如加法、减法、乘法、除法等。"
        "输入应该是一个数学表达式，例如'200*7'或'5000/2*10'。"
    )

    def _run(self, operation: str) -> float:
        try:
            # 定义允许的安全运算符
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }

            # 解析和验证表达式
            if not re.match(r'^[0-9+\-*/().% ]+$', operation):
                raise ValueError("数学表达式中包含无效字符")

            # 解析表达式
            tree = ast.parse(operation, mode='eval')

            def _eval_node(node):
                if isinstance(node, ast.Expression):
                    return _eval_node(node.body)
                elif isinstance(node, ast.Constant):  # Python 3.8+
                    return node.value
                elif isinstance(node, ast.Num):  # Python < 3.8
                    return node.n
                elif isinstance(node, ast.BinOp):
                    left = _eval_node(node.left)
                    right = _eval_node(node.right)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"不支持的运算符: {type(node.op).__name__}")
                    return op(left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = _eval_node(node.operand)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"不支持的运算符: {type(node.op).__name__}")
                    return op(operand)
                else:
                    raise ValueError(f"不支持的节点类型: {type(node).__name__}")

            result = _eval_node(tree)
            return result

        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
            raise ValueError(f"计算错误: {str(e)}")
        except Exception:
            raise ValueError("无效的数学表达式")