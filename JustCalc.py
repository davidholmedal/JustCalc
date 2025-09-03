import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import sys
import math
import re

class JustCalc:
    """A calculator application using ttk widgets."""
    
    def __init__(self):
        """Initialize the calculator application."""
        
        # Variables dictionary to store user-defined variables
        self.variables = {
            'pi': math.pi,
            'e': math.e
        }


        # Configure dark mode colors
        self.bg_color = '#2b2b2b'  # Dark background
        self.fg_color = '#ffffff'  # White text
        self.medium_color = "#5f5f5f" #medium
        self.text_bg = '#3c3f41'   # Slightly lighter dark for text areas
        self.text_fg = '#ffffff'   # White text in text areas
        self.insert_color = '#ffffff'  # White cursor
        self.select_bg = '#4c5052'  # Selection background
        self.border_color = "#000000" #border
        self.arrow_color = self.fg_color #arrow


        self.window = tk.Tk()
        self.style = ttk.Style()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window properties."""

        self.window.title("JustCalc")
        self.window.geometry("600x200")
        self.window.resizable(True, True)
        
        # Apply dark theme to main window
        self.window.configure(bg=self.bg_color)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        
    def create_widgets(self):
        """Create and arrange all the widgets."""
        """ 
        self.frame_left = tk.Frame(self.window, bg=self.bg_color)
        self.frame_middle = tk.Frame(self.window, bg=self.bg_color)
        self.frame_right = tk.Frame(self.window, bg=self.bg_color)

        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_middle.grid(row=0, column=1, sticky="nsew")
        self.frame_right.grid(row=0, column=2, sticky="nsew")
        """

        # Make columns expand
        self.window.grid_columnconfigure(0, weight=2, minsize=100) 
        self.window.grid_columnconfigure(1, weight=1, minsize=20)  
        self.window.grid_columnconfigure(2, weight=0)  
        self.window.grid_rowconfigure(0, weight=1)
        

        # Create text widgets with dark theme
        self.expression_text = tk.Text(
            self.window,
            height=5, 
            #width=50,
            bg=self.text_bg,
            fg=self.text_fg,
            insertbackground=self.insert_color,
            selectbackground=self.select_bg,
            selectforeground=self.text_fg,
            relief='flat',
            borderwidth=0,
            font=('Consolas', 10)
        )
        
        self.answer_text = tk.Text(
            #self.frame_middle, 
            self.window,
            height=5, 
            #width=25,
            bg=self.text_bg,
            fg=self.text_fg,
            insertbackground=self.insert_color,
            selectbackground=self.select_bg,
            selectforeground=self.text_fg,
            relief='flat',
            borderwidth=0,
            font=('Consolas', 10)
        )
        
         # Style the scrollbar
        self.style.configure("Custom.Vertical.TScrollbar",
            gripcount=0,
            background=self.medium_color,   # the thumb color
            darkcolor=self.medium_color,    # shadow
            lightcolor=self.medium_color,   # highlight
            troughcolor=self.bg_color,      # track color
            bordercolor=self.border_color,  
            arrowcolor=self.arrow_color     
        )
        self.scrollbar = ttk.Scrollbar(
            #self.frame_right, 
            self.window, 
            style="Custom.Vertical.TScrollbar"
        )




        # Pack widgets with proper spacing for dark theme
        padding = 4
        #self.expression_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=(4,4), pady=10)
        #self.answer_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, padx=(0,4), pady=10)
        #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,4), pady=10)

        
        self.expression_text.grid(row=0, column=0, sticky="nsew")
        self.answer_text.grid(row=0, column=1, sticky="nsew")
        self.scrollbar.grid(row=0, column=2, sticky="nsew")

        

        # Function to sync scrolling
        def sync_scroll(*args):
            # Update scrollbar position
            self.scrollbar.set(*args)
            

        def scroll_both(*args):
            # Synchronize both text widgets when scrollbar is moved
            self.expression_text.yview(*args)
            self.answer_text.yview(*args)
            self.update_scrollbar_visibility()

        # Connect scrollbar to both texts
        self.scrollbar.config(command=scroll_both)
        self.expression_text.config(yscrollcommand=sync_scroll)
        self.answer_text.config(yscrollcommand=sync_scroll)

        # Bind the evaluate function to key release
        self.expression_text.bind('<KeyRelease>', self.evaluate_expressions)
        
        # Bind window resize to update scrollbar visibility
        self.window.bind('<Configure>', self.delayed_scrollbar_check)


    def sync_scroll_positions(self):
        """Synchronize the scroll positions of both text widgets."""
        try:
            # Get current scroll position from expression text
            current_pos = self.expression_text.yview()
            # Apply same position to answer text
            self.answer_text.yview_moveto(current_pos[0])
        except Exception:
            pass  # Ignore any scroll-related errors
    

    def needs_scrollbar(self, text):
        """Checks vertical size"""
        font = tkFont.Font(font=text['font'])
        font_height = font.metrics("linespace")
        print("Font height:", font_height)

        visible_lines = text.winfo_height() // font_height
        total_lines = int(text.index("end-1c").split(".")[0])

        if total_lines > visible_lines:
            print("Vertical overflow detected")
            return True
        return False



    def update_scrollbar_visibility(self, event=None):
        """Check if scrollbar should be visible and show/hide accordingly."""
        print("check scrollbar vis")

        if self.needs_scrollbar(self.expression_text):
            print("needs scrollbar")
            #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
            self.scrollbar.grid(row=0, column=2, sticky="ns")
        else:
            self.scrollbar.grid_forget()
            #self.scrollbar.pack_forget()
    
    
    def evaluate_expressions(self, event=None):
        # Get all lines from input
        input_lines = self.expression_text.get("1.0", tk.END).split('\n')
        # Remove the last empty line that tk.END creates
        if input_lines and input_lines[-1] == '':
            input_lines.pop()

        # Clear output
        self.answer_text.config(state='normal')
        self.answer_text.delete("1.0", tk.END)
        
        results = []
        
        for line in input_lines:
            line = line.strip()
            if not line:
               results.append("")
               continue
                
            # Check for variable assignment
            var_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', line)
            if var_match:
                var_name, expr = var_match.groups()
                try:
                    result = self._evaluate_expression(expr)
                    self.variables[var_name] = result
                    results.append(f"{var_name} = {result}")
                except Exception as e:
                    #results.append(f"Error: {str(e)}")
                    results.append("Unknown variable")
                continue
                
            # Evaluate regular expression
            try:
                result = self._evaluate_expression(line)
                results.append(str(result))
            except Exception as e:
                #results.append(f"Error: {str(e)}")
                results.append("Syntax Error")
        
        # Update output text
        self.answer_text.insert(tk.END, '\n'.join(results))
        self.answer_text.config(state='disabled')
        
        # Sync scroll position with expression text
        self.sync_scroll_positions()
        
        # Check if scrollbar should be visible
        self.delayed_scrollbar_check()
    


    def delayed_scrollbar_check(self, event=None):
        """Check scrollbar visibility after a short delay to ensure widget updates are complete."""
        self.window.after(100, self.update_scrollbar_visibility)
    
    def _evaluate_expression(self, expr):
        # Replace variable names with their values
        for var_name, value in self.variables.items():
            # Use word boundaries to avoid partial matches
            expr = re.sub(r'\b' + re.escape(var_name) + r'\b', str(value), expr)
        
        # Replace ^ with ** for exponentiation
        expr = expr.replace('^', '**')
        
        # Add math module functions to the local namespace
        local_vars = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log10,  # Using log10 as log to match calculator convention
            'ln': math.log,     # Natural logarithm
            'exp': math.exp,
            'radians': math.radians,
            'degrees': math.degrees,
            'abs': abs,
            'round': round,
            'pi': math.pi,
            'e': math.e
        }
        
        try:
            # Evaluate the expression safely
            result = eval(expr, {"__builtins__": {}}, local_vars)
            # Convert to integer if it's a whole number for cleaner display
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            raise ValueError(f"Could not evaluate: {expr}")


    def run(self):
        """Start the application main loop."""
        self.window.mainloop()
        


def main():
    """Main entry point for the application."""
    try:
        app = JustCalc()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

