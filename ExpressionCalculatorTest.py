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
        print("\n\nRunning ExpressionCalculator tests")
        tests = self._get_tests()
        failed_test_names = []
        i=1
        for name, t in tests.items():
            print(f"\n\nRunning test {i} of {len(tests)}...")
            
            if not (result := t()):
                failed_test_names.append({'name': name, 'num': i})

            i += 1
        
        if len(failed_test_names) == 0:
            print(f"\n\nTesting finished. Successfully! {len(tests)} tests")
        else:
            print(f"\n\nTesting finished. Failed {len(failed_test_names)}/{len(tests)}")
            for t in failed_test_names:
                print(f"    {t['num']}:    {t['name']}")

    
    # Decorator
    def test_state(func):
        def wrapper(self):
            print(f"START {func.__name__}")
            try:
                func(self)
            except Exception as e:
                print(f"FAILED! {func.__name__}")
                return False
            print(f"SUCCESS! {func.__name__}")
            return True
        return wrapper


    ### Test declarations below ###
    @test_state
    def test_addition(self):
            calc = ExpressionCalculator()
            res = calc.calculate("5+5")
            if res != '10':
                raise Exception(f"failed addition: {res}")
        

    @test_state
    def test_subtraction(self):
        calc = ExpressionCalculator()
        res = calc.calculate("10-5")
        if res != '5': 
            raise Exception(f"failed subtraction: {res}")


    @test_state
    def test_multiplication(self):
        calc = ExpressionCalculator()
        res = calc.calculate("5*5")
        if res != '25': 
            raise Exception(f"failed multiplication: {res}")
    

    @test_state
    def test_division(self):
        calc = ExpressionCalculator()
        res = calc.calculate("25/5")
        if res != '5': 
            raise Exception(f"failed multiplication: {res}")
    

    @test_state
    def test_syntax_error(self):
        calc = ExpressionCalculator()
        res = calc.calculate("25sdferw")
        if res.lower().find("syntax error"): 
            raise Exception(f"failed syntax error test: {res}")
    

    @test_state
    def test_unknown_variable(self):
        calc = ExpressionCalculator()
        res = calc.calculate("x")
        if res.lower() != "Contains undeclared variable".lower(): 
            raise Exception(f"failed unknown variable test: {res}")


    @test_state
    def test_variable_assignment(self):
        calc = ExpressionCalculator()
        res = calc.calculate("x=5")
        if res != '5': 
            raise Exception(f"failed variable assignment test: {res}")


    @test_state
    def test_set_use_degrees(self):
        calc = ExpressionCalculator()
        calc.set_use_degrees(True)
        
        print(f"get_use_degrees() = {calc.get_use_degrees()}")

        if not calc.get_use_degrees(): 
            raise Exception(f"failed to set use degrees to True")


    @test_state
    def test_set_use_radians(self):
        calc = ExpressionCalculator()
        calc.set_use_degrees(False)
        
        print(f"get_use_degrees() = {calc.get_use_degrees()}")

        if calc.get_use_degrees(): 
            raise Exception(f"failed to set use degrees to False")


    @test_state
    def test_use_degrees(self):
        calc = ExpressionCalculator()
        calc.set_use_degrees(True)
        res = calc.calculate("cos(180)")
        if int(res) != -1: 
            raise Exception(f"failed use degrees test: {res}")


    @test_state
    def test_use_radians(self):
        calc = ExpressionCalculator()
        calc.set_use_degrees(False)
        res = calc.calculate("cos(pi)")
        if int(res) != -1: 
            raise Exception(f"failed use radians test: {res}")


    @test_state
    def test_does_contain_undeclared_variable(self):
        calc = ExpressionCalculator()
        #NOTE! should really be one test method for each case.
        test_expressions = [
            "x", "a", "some_word", "var1", "xyz12", "ab12cd", "sin(a)", "5*a", "some_word*5"
        ]
        
        failed_tests = []
        for expr in test_expressions:
            res = calc._contains_undeclared_variable(expr)  #should return true
            if not res: 
                # failed because it returns false when expression DOES contain undeclared variable
                print(f" failed because it returns false when expression DOES contain undeclared variable: {expr}")
                failed_tests.append(expr)
                
        if failed_tests:
            raise Exception(f"  failed DOES contain undeclared variable test: {failed_tests}")


    @test_state
    def test_does_not_contain_undeclared_variable(self):
        calc = ExpressionCalculator()
        #NOTE! should really be one test method for each case.
        test_variables_declarations = [
            "x=1", "a=2", "some_word=3", "var1=4", "xyz12=5", "ab12cd=6"
        ]

        test_expressions = [
            "x", "a", "some_word", "var1", "xyz12", "ab12cd", "sin(a)", "5*a", "some_word*5"
        ]

        # add the variable declarations to calc first
        for expr in test_variables_declarations:
            calc.calculate(expr)

        failed_tests = []
        for expr in test_expressions:
            res = calc._contains_undeclared_variable(expr)  #should return false
            if res: 
                # failed because it returns True when expression does NOT contain undeclared variable
                print(f" failed because it returns TRUE when expression DOES NOT contain undeclared variable: {expr}")
                failed_tests.append(expr)
                
        if failed_tests:
            raise Exception(f"  failed DOES NOT contain undeclared variable test: {failed_tests}")        


        