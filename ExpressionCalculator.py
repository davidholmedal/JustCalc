import math
import re
import string


class ExpressionCalculator:
    def __init__(self, use_degrees: bool = False) -> None:
        
        self.precision = 6
        self.use_degrees= use_degrees
        
        self.user_vars = {
            
        }

        # Local math functions
        self.math_vars = {
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'exp': math.exp,
            'radians': math.radians,
            'degrees': math.degrees,
            'abs': (lambda x: abs(x)),
            'round': (lambda x: round(x)),
            'pi': math.pi,
            'e': math.e,
        }

        self.math_vars_degrees = {
            'sin': (lambda x: math.sin(math.radians(x))),
            'cos': (lambda x: math.cos(math.radians(x))),
            'tan': (lambda x: math.tan(math.radians(x))),
        }

        self.math_vars_radians = {
            'sin': (lambda x: math.sin(x)),
            'cos': (lambda x: math.cos(x)),
            'tan': (lambda x: math.tan(x)),
        }

        self.math_vars_degrees.update(self.math_vars)
        self.math_vars_radians.update(self.math_vars)
    

    def set_use_degrees(self, state):
        self.use_degrees = state


    def get_use_degrees(self):
        return self.use_degrees


    def _do_variable_assignment(self, expression):
        var_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', expression)

        if var_match:
            var_name, expr = var_match.groups()

            try:
                result = self._calculate(expr)
                self.user_vars[var_name] = result
                
                return True, result
            except Exception as e:
                print("\n\t exception in variable assignment")
        
        return False, 0
        
    
    def _find_free_vars(self, expr, _vars):
        candidates = set(re.findall(r'\b[A-Za-z_]\w*\b', expr))
        undeclared_vars = sorted(name for name in candidates if name not in _vars)
        return undeclared_vars


    def _contains_undeclared_variable(self, expression):
        res = self._find_free_vars(expression, self._get_vars())
        
        if res:
            return True
        else:
            return False


    def _get_vars(self):
        if self.get_use_degrees():
            vars = self.math_vars_degrees.copy()
            vars.update(self.user_vars)
            return vars
        else:
            vars = self.math_vars_radians.copy()
            vars.update(self.user_vars)
            return vars
        


    def _calculate(self, expression):
        print(f"_calculate({expression})")
        try:
            result = eval(expression, {"__builtins__": {}}, self._get_vars())
            print(f"    result::{result}  {type(result)}")

            if isinstance(result, str):
                print(f"    eval is string result:{result}")

            
            if isinstance(result, int):
                return str(result)

            
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                
                # format float to fixed precision, strip trailing zeros but keep at least one decimal point
                formatted = f"{result:.{self.precision}f}"
                result = formatted
                return str(result)

            if isinstance(result, str):
                return result

        except Exception as e:
            raise ValueError(f"Could not evaluate: {expression}") from e
    



    def calculate(self, expression: str):
        
        # Cleanup input string
        if expression is None:
            raise ValueError("expression is None")

        expression = expression.strip()

        # Is expression an empty string?
        if not expression:
            return ''

        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        
        # first evaluate if it is a variable assignment, continue regardless
        success, res = self._do_variable_assignment(expression)
        if success:
            return str(res)
        
        # has undeclared variable
        res = self._contains_undeclared_variable(expression)
        if res:
            return "Contains undeclared variable"
        

        # Evaluate a 'normal' expression
        try:
            result = self._calculate(expression)
            print(f"result = {result}")
            return result
        except Exception as e:
            return f"Syntax Error e={e}"







