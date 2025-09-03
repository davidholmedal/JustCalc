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
        self.black = "#000000"
        self.text_color = "#ffffff"
        self.light_color = "#9f9f9f"
        self.medium_color = "#222222"
        self.dark_color = "#2b2b2b"
        self.accent_color = "#5f5f5f"
        self.light_accent_color = "#bb2200"
        self.medium_accent_color = "#664400"
        self.dark_accent_color = "#000000"

        self.border_thickness = 1
        self.padding = 4
        self.text_size = 11
        self.font = 'Consolas'
        self.precision = 6
        self.default_height_lines = 5

        self.bg_color = self.dark_color
        self.fg_color = self.text_color  # text
        
        self.text_bg = self.medium_color   # Slightly lighter dark for text areas
        self.text_fg = self.text_color   # White text in text areas
        self.select_bg_color=self.light_color,
        self.select_fg_color=self.dark_color,
        self.insert_color = self.text_color  # White cursor
        self.select_bg = self.light_color  # Selection background
        self.border_color = self.light_color
        self.border_selected_color = self.light_accent_color
        self.arrow_color = self.text_color #arrow

        


        self.window = tk.Tk()
        self.style = ttk.Style()
        
        # Angle mode (False=radians, True=degrees)
        self.use_degrees = tk.BooleanVar(value=False)
        
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
        self.window.grid_columnconfigure(0, weight=8, minsize=200)
        self.window.grid_columnconfigure(1, weight=8, minsize=200)  
        self.window.grid_columnconfigure(2, weight=0)  
        self.window.grid_rowconfigure(0, weight=1)
        

        # Create text widgets with dark theme
        self.expression_text = tk.Text(
            self.window,
            height=self.default_height_lines, 
            width=150,
            bg=self.text_bg,
            fg=self.text_fg,
            highlightthickness=self.border_thickness,
            highlightcolor=self.border_selected_color,
            highlightbackground=self.border_color,
            insertbackground=self.insert_color,
            selectbackground=self.select_bg,
            selectforeground=self.text_fg,
            relief='flat',
            borderwidth=0,
            font=(self.font, self.text_size)
        )
        
        self.answer_text = tk.Text(
            #self.frame_middle, 
            self.window,
            height=self.default_height_lines, 
            width=100,
            bg=self.text_bg,
            fg=self.text_fg,
            highlightthickness=self.border_thickness,
            highlightcolor=self.border_selected_color,
            highlightbackground=self.border_color,
            insertbackground=self.insert_color,
            selectbackground=self.select_bg,
            selectforeground=self.text_fg,
            relief='flat',
            borderwidth=0,
            state='disabled',
            takefocus=0,
            cursor='arrow',
            font=(self.font, self.text_size)
        )
        
         # Style the scrollbar
        self.style.configure("Custom.Vertical.TScrollbar",
            gripcount=0,
            background=self.light_color,   # the thumb color
            darkcolor=self.medium_color,    # shadow
            lightcolor=self.medium_color,   # highlight
            troughcolor=self.bg_color,      # track color
            bordercolor=self.black,  
            arrowcolor=self.arrow_color     
        )
        self.scrollbar = ttk.Scrollbar(
            #self.frame_right, 
            self.window, 
            style="Custom.Vertical.TScrollbar"
        )

        self.expression_text.tag_configure('sel', background=self.select_bg_color, foreground=self.select_fg_color)
        self.answer_text.tag_configure('sel', background=self.select_bg_color, foreground=self.select_fg_color)


        # Pack widgets with proper spacing for dark theme
        
        #self.expression_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=(4,4), pady=10)
        #self.answer_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, padx=(0,4), pady=10)
        #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,4), pady=10)

        
        self.expression_text.grid(row=0, column=0, sticky="nsew", padx=(self.padding,self.padding), pady=self.padding)
        self.answer_text.grid(row=0, column=1, sticky="nsew", padx=(0,self.padding), pady=self.padding)
        self.scrollbar.grid(row=0, column=2, sticky="ns")

        # Angle mode toggle row
        self.degrees_check = tk.Checkbutton(
            self.window,
            text="Use Degrees",
            variable=self.use_degrees,
            onvalue=True,
            offvalue=False,
            bg=self.bg_color,
            fg=self.text_fg,
            activebackground=self.bg_color,
            activeforeground=self.text_fg,
            selectcolor=self.bg_color,
            highlightthickness=0,
            command=lambda: self.evaluate_expressions()
        )
        self.degrees_check.grid(row=1, column=0, sticky="w", padx=self.padding, pady=(0, self.padding))

        # Info label below editors
        self.info_label = tk.Label(
            self.window,
            text="""Type expressions on the left. Results appear on the right. 
Supports trig functions like sin(x), cos(x), variables x=5, x^2 and more.""",
            bg=self.bg_color,
            fg=self.light_color,
            anchor='w',
            justify='left'
        )
        self.info_label.grid(row=2, column=0, columnspan=3, sticky="ew", padx=self.padding, pady=(0, self.padding))

        

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

        

        def _select_expression_initial():
            self.expression_text.focus_set()
            #self.expression_text.tag_add("sel", "1.0", "end-1c")
            #self.expression_text.mark_set("insert", "end-1c")

        self.window.after(0, _select_expression_initial)


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
                if isinstance(result, float):
                    # format float to fixed precision, strip trailing zeros but keep at least one decimal point
                    formatted = f"{result:.{self.precision}f}"
                    results.append(formatted)
                else:
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
            'sin': (lambda x: math.sin(math.radians(x))) if self.use_degrees.get() else math.sin,
            'cos': (lambda x: math.cos(math.radians(x))) if self.use_degrees.get() else math.cos,
            'tan': (lambda x: math.tan(math.radians(x))) if self.use_degrees.get() else math.tan,
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

