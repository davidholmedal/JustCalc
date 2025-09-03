import math
import re


class ExpressionCalculator:
    def __init__(self, use_degrees: bool = False) -> None:
        """Initialize calculator configuration.

        Args:
            use_degrees: If True, trig functions interpret inputs as degrees.
        """
        self.use_degrees: bool = use_degrees
        self.variables = {
            'pi': math.pi,
            'e': math.e
        }



    def _calculate(self, expression):
        """Evaluate a mathematical expression and return the result.

        Supports ^ for exponentiation and common math functions. If
        use_degrees is True, sin/cos/tan interpret the value in degrees.
        """
        if expression is None:
            raise ValueError("expression must be a string")

        expr = expression.strip()
        if not expression:
            return ''


        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')

        # Local math functions with optional degree handling
        local_vars = {
            'sin': (lambda x: math.sin(math.radians(x))) if self.use_degrees else math.sin,
            'cos': (lambda x: math.cos(math.radians(x))) if self.use_degrees else math.cos,
            'tan': (lambda x: math.tan(math.radians(x))) if self.use_degrees else math.tan,
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'exp': math.exp,
            'radians': math.radians,
            'degrees': math.degrees,
            'abs': abs,
            'round': round,
            'pi': math.pi,
            'e': math.e,
        }

        try:
            result = eval(expression, {"__builtins__": {}}, local_vars)
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as exc:
            raise ValueError(f"Could not evaluate: {expression}") from exc


    def calculate(self, expression: str):
        
        var_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', expression)
        if var_match:
            var_name, expr = var_match.groups()
            try:
                result = self._calculate(expr)
                self.variables[var_name] = result
                return f"{var_name} = {result}"
            except Exception as e:
                return "Unknown variable"
        else:
            # Evaluate regular expression
            try:
                #result = self._evaluate_expression(line)
                result = self._calculate(expression)
                if isinstance(result, float):
                    # format float to fixed precision, strip trailing zeros but keep at least one decimal point
                    formatted = f"{result:.{self.precision}f}"
                    return formatted
                else:
                    return str(result)
            except Exception as e:
                #results.append(f"Error: {str(e)}")
                return "Syntax Error"






