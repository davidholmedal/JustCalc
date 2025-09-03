from ExpressionCalculator import ExpressionCalculator


class ExpressionCalculatorTest:
    def __init__(self) -> None:
        print("Init ExpressionCalculator Testing")
    

    def _get_tests(self):
        return {
            name: getattr(self, name)
            for name in dir(self)
            if name.startswith("test_") and callable(getattr(self, name))
        }


    def run_tests(self):
        print("Running ExpressionCalculator tests")
        tests = self._get_tests()
        
        i=0
        failed = 0
        for name, t in tests.items():
            print(f"running test {i} of {len(tests)} {name}...")
            
            try:
                t()
            except Exception as e:
                failed += 1
                print(f"{e}")

            i += 1
        
        if failed == 0:
            print(f"Testing finished. Successfully! {len(tests)} tests")
        else:
            print(f"Testing finished. Failed {failed}/{len(tests)}")


    def test_addition(self):
            calc = ExpressionCalculator()
            res = calc.calculate("5+5")
            if int(res) != 10: 
                raise Exception(f"failed addition: {res}")
        
    def test_subtraction(self):
        calc = ExpressionCalculator()
        res = calc.calculate("10-5")
        if int(res) != 5: 
            raise Exception(f"failed subtraction: {res}")

    def test_multiplication(self):
        calc = ExpressionCalculator()
        res = calc.calculate("5*5")
        if int(res) != 25: 
            raise Exception(f"failed multiplication: {res}")
    
    def test_division(self):
        calc = ExpressionCalculator()
        res = calc.calculate("25/5")
        if int(res) != 5: 
            raise Exception(f"failed multiplication: {res}")
    
    def test_syntax_error(self):
        calc = ExpressionCalculator()
        res = calc.calculate("25sdferw")
        if res.lower() != "syntax error": 
            raise Exception(f"failed syntax error test: {res}")
    
    def test_unknown_variable(self):
        calc = ExpressionCalculator()
        res = calc.calculate("25sdferw")
        if res.lower() != "unknown variable": 
            raise Exception(f"failed syntax error test: {res}")