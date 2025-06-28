"""
Calculator tool implementation for MCP server
"""

import ast
import operator
import math
from typing import Any, Dict, Union
from dataclasses import dataclass


@dataclass
class CalculationResult:
    """Result of a calculation operation"""
    expression: str
    result: Union[float, int, str]
    success: bool
    error: str = None


class SafeCalculator:
    """Safe calculator that evaluates mathematical expressions using AST parsing"""
    
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    functions = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'pow': pow,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'ceil': math.ceil,
        'floor': math.floor,
        'pi': math.pi,
        'e': math.e,
    }
    
    def evaluate(self, expression: str) -> CalculationResult:
        """Safely evaluate a mathematical expression
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            CalculationResult with the result or error information
        """
        try:
            node = ast.parse(expression, mode='eval')
            result = self._eval_node(node.body)
            
            return CalculationResult(
                expression=expression,
                result=result,
                success=True
            )
            
        except ZeroDivisionError:
            return CalculationResult(
                expression=expression,
                result=None,
                success=False,
                error="Division by zero"
            )
        except (ValueError, TypeError) as e:
            return CalculationResult(
                expression=expression,
                result=None,
                success=False,
                error=f"Math error: {str(e)}"
            )
        except SyntaxError:
            return CalculationResult(
                expression=expression,
                result=None,
                success=False,
                error="Invalid mathematical expression"
            )
        except Exception as e:
            return CalculationResult(
                expression=expression,
                result=None,
                success=False,
                error=f"Calculation error: {str(e)}"
            )
    
    def _eval_node(self, node: ast.AST) -> Union[float, int]:
        """Recursively evaluate an AST node"""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op(operand)
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name not in self.functions:
                raise ValueError(f"Unsupported function: {func_name}")
            
            args = [self._eval_node(arg) for arg in node.args]
            func = self.functions[func_name]
            
            if func_name in ['min', 'max', 'sum'] and len(args) == 1 and isinstance(args[0], (list, tuple)):
                return func(args[0])
            else:
                return func(*args)
        elif isinstance(node, ast.Name):
            if node.id in self.functions:
                value = self.functions[node.id]
                if callable(value):
                    raise ValueError(f"Function {node.id} requires arguments")
                return value
            else:
                raise ValueError(f"Undefined variable: {node.id}")
        elif isinstance(node, ast.List):
            return [self._eval_node(item) for item in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(self._eval_node(item) for item in node.elts)
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")


_calculator = SafeCalculator()


def calculate(expression: str) -> CalculationResult:
    """Calculate a mathematical expression safely
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        CalculationResult with the result or error information
    """
    return _calculator.evaluate(expression)
