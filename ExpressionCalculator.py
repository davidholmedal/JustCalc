import math
import re
import string


class ExpressionCalculator:
    def __init__(self, use_degrees: bool = False) -> None:
        
        self.precision: int = 6
        self.use_degrees: bool = use_degrees
        self.user_vars: dict[str, object] = {}
        self.math_vars: dict[str, object] = {
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
        
        self.math_vars_radians: dict[str, object] = self.math_vars | {
            'sin': (lambda x: math.sin(x)),
            'cos': (lambda x: math.cos(x)),
            'tan': (lambda x: math.tan(x)),
        }

        self.math_vars_degrees: dict[str, object] = self.math_vars | {
            'sin': (lambda x: math.sin(math.radians(x))),
            'cos': (lambda x: math.cos(math.radians(x))),
            'tan': (lambda x: math.tan(math.radians(x))),
        }
        

    def set_use_degrees(self, state: bool = True) -> None:
        self.use_degrees = state


    def get_use_degrees(self) -> bool:
        return self.use_degrees


    def _do_variable_assignment(self, expression: str = "")-> tuple[bool, str]:
        var_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', expression)

        if var_match:
            var_name, expr = var_match.groups()

            try:
                result = self._calculate(expr)
                self.user_vars[var_name] = result
                
                return True, result
            except Exception as e:
                print("\n\t exception in variable assignment")
        
        return False, ''
        
    
    def _find_free_vars(self, expr: str = "", _vars: dict[str, object] = {}) -> list[str]:
        candidates = set(re.findall(r'\b[A-Za-z_]\w*\b', expr))
        undeclared_vars = sorted(name for name in candidates if name not in _vars)
        return undeclared_vars


    def _contains_undeclared_variable(self, expression: str = "") -> bool:
        res = self._find_free_vars(expression, self._get_vars())
        
        if res:
            return True
        else:
            return False


    def _get_vars(self) -> dict[str, object]:
        if self.get_use_degrees():
            vars = self.math_vars_degrees.copy()
            vars.update(self.user_vars)
            return vars
        else:
            vars = self.math_vars_radians.copy()
            vars.update(self.user_vars)
            return vars
        


    def _calculate(self, expression: str = "") -> str:
        #print(f"_calculate({expression})")
        try:
            result = eval(expression, {"__builtins__": {}}, self._get_vars())
            print(f"    {result = } {type(result)}")

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

        return ""


    def calculate(self, expression: str = "") -> str:
        
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
        #res_ = self._contains_undeclared_variable(expression)
        #if res_:
        if self._contains_undeclared_variable(expression):
            return "Contains undeclared variable"
        

        # Evaluate a 'normal' expression
        try:
            result = self._calculate(expression)
            #print(f"{result =}")
            return result
        except Exception as e:
            return f"Syntax Error e={e}"







