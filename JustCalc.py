import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import sys
from ExpressionCalculator import ExpressionCalculator
from ExpressionCalculatorTest import ExpressionCalculatorTest
from JustCalcView import JustCalcView


class JustCalc:
    
    def __init__(self, calculator: ExpressionCalculator) -> None:
        self.calculator: ExpressionCalculator = calculator
        self.view = JustCalcView()
        self.view.add_listener(self.evaluate_expressions)

    
    
    def evaluate_expressions(self, input_lines: list[str], use_degrees: bool = True) -> list[str]:
        results: list[str] = []
        
        for line in input_lines:
            line = line.strip()
            if not line:
               results.append("")
               continue
            
            print(f"{line = }")
            self.calculator.set_use_degrees(use_degrees)
            result = str(self.calculator.calculate(line))
            results.append(result)
        
        return results



    def run(self) -> None:
        self.view.run()
    


def main() -> None:
    try:
        tests = ExpressionCalculatorTest()
        tests.run_tests()

        calculator = ExpressionCalculator(True)
        app = JustCalc(calculator)
        app.run()

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

