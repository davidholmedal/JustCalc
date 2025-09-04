import math
from pickle import FALSE
import re


class ExpressionCalculator:
    def __init__(self, use_degrees: bool = False) -> None:
        """Initialize calculator configuration.

        Args:
            use_degrees: If True, trig functions interpret inputs as degrees.
        """
        self.precision = 6
        self.use_degrees= use_degrees
        
        
        # Local math functions with optional degree handling
        self.local_vars = {
            'sin': (lambda x: math.sin(math.radians(x))) if self.get_use_degrees() else math.sin,
            'cos': (lambda x: math.cos(math.radians(x))) if self.get_use_degrees() else math.cos,
            'tan': (lambda x: math.tan(math.radians(x))) if self.get_use_degrees() else math.tan,
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

        #self.local_vars = {


        self.user_vars = {
            
        }
    

    def set_use_degrees(self, state):
        self.use_degrees = state


    def get_use_degrees(self):
        return self.use_degrees


    def _do_variable_assignment(self, expression):
        print(f"_do_variable_assignment({expression})")
        var_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', expression)
        print(f" after re.match {var_match}")

        if var_match:
            print("\n\texpression contains variable assignment")
            var_name, expr = var_match.groups()

            try:
                print(f"\tvar_name={var_name} expr={expr}")
                result = self._calculate(expr)
                self.local_vars[var_name] = result
                print(f"\t{var_name} = {result}")
                #return f"{var_name} = {result}"
                return True, result
            except Exception as e:
                print("\n\t exception in variable assignment")
        
        return False, 0
        
    
    def _find_free_vars(self, expr, _vars):
        candidates = set(re.findall(r'\b[A-Za-z_]\w*\b', expr))
        print(f"  candidates: {candidates}")
        undeclared_vars = sorted(name for name in candidates if name not in _vars)
        print(f"  undeclared_vars: {undeclared_vars}")
        return undeclared_vars


    def _contains_undeclared_variable(self, expression):
        print(f"  _contains_undeclared_variable({expression})")
        res = self._find_free_vars(expression, self.local_vars)
        print(f"        undeclared vars len(res)={len(res)}   res: {res}")
        if res:
            print(f"        undeclared vars TRUE")
            return True
        else:
            print(f"        undeclared vars FALSE")
            return False


    def _calculate(self, expression):
        """Evaluate a mathematical expression and return the result.

        Supports ^ for exponentiation and common math functions. If
        use_degrees is True, sin/cos/tan interpret the value in degrees.
        """
                
        print(f"_calculate expression={expression}")
        
        
        self.local_vars = {
            'sin': (lambda x: math.sin(math.radians(x))) if self.get_use_degrees() else math.sin,
            'cos': (lambda x: math.cos(math.radians(x))) if self.get_use_degrees() else math.cos,
            'tan': (lambda x: math.tan(math.radians(x))) if self.get_use_degrees() else math.tan,
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
            result = eval(expression, {"__builtins__": {}}, self.local_vars)
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            print(f"\n\t exception in _calc: {e}")
            raise ValueError(f"Could not evaluate: {expression}") from e


    def calculate(self, expression: str):
        print(f"\n calculate({expression})")

        # Cleanup input string
        if expression is None:
            print(f"expression is None{expression}")
            raise ValueError("expression must be a string")

        expression = expression.strip()

        print(f"after strip:{expression}")
        # Is expression an empty string?
        if not expression:
            return ''

        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        print(f"after replace ^ **:{expression}")


        # first evaluate if it is a variable assignment, continue regardless
        success, res = self._do_variable_assignment(expression)
        if success:
            print(f"variable assignment expr:{expression} result={res}")
            return str(res)
        else:
            print(f"No variable assignment {expression}")
            

        
        res = self._contains_undeclared_variable(expression)
        if res:
            print("Contains undeclared variable")
            return "Contains undeclared variable"
        else:
            # Evaluate a 'normal' expression
            print(f"        Doing normal calc: {expression}")

            try:
                result = self._calculate(expression)
                if isinstance(result, float):
                    # format float to fixed precision, strip trailing zeros but keep at least one decimal point
                    formatted = f"{result:.{self.precision}f}"
                    return formatted
                else:
                    return str(result)
            except Exception as e:
                #results.append(f"Error: {str(e)}")
                return f"Syntax Error e={e}"






