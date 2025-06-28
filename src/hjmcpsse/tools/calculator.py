import ast
import operator
from typing import Union, Dict, Any
from pydantic import BaseModel


class CalculationResult(BaseModel):
    expression: str
    result: Union[float, int]
    success: bool
    error: str = ""


class SafeCalculator:
    """Safe calculator that evaluates mathematical expressions"""
    
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    ALLOWED_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
    }
    
    def evaluate(self, expression: str) -> CalculationResult:
        """Safely evaluate a mathematical expression"""
        try:
            expression = expression.strip()
            if not expression:
                return CalculationResult(
                    expression=expression,
                    result=0,
                    success=False,
                    error="Empty expression"
                )
            
            tree = ast.parse(expression, mode='eval')
            result = self._eval_node(tree.body)
            
            return CalculationResult(
                expression=expression,
                result=result,
                success=True
            )
        
        except (SyntaxError, ValueError) as e:
            return CalculationResult(
                expression=expression,
                result=0,
                success=False,
                error=f"Invalid expression: {str(e)}"
            )
        except ZeroDivisionError:
            return CalculationResult(
                expression=expression,
                result=0,
                success=False,
                error="Division by zero"
            )
        except Exception as e:
            return CalculationResult(
                expression=expression,
                result=0,
                success=False,
                error=f"Calculation error: {str(e)}"
            )
    
    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        """Recursively evaluate AST nodes"""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            
            if op_type not in self.ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            
            return self.ALLOWED_OPERATORS[op_type](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            
            if op_type not in self.ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            
            return self.ALLOWED_OPERATORS[op_type](operand)
        
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            
            if func_name not in self.ALLOWED_FUNCTIONS:
                raise ValueError(f"Unsupported function: {func_name}")
            
            args = [self._eval_node(arg) for arg in node.args]
            return self.ALLOWED_FUNCTIONS[func_name](*args)
        
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")


def calculate(expression: str) -> CalculationResult:
    """Calculate the result of a mathematical expression"""
    calculator = SafeCalculator()
    return calculator.evaluate(expression)
