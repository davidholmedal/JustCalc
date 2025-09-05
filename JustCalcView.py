import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from typing import Any


from Style import Style
from TextBoxView import TextBoxView
from ScrollBarView import ScrollBarView
from CheckBoxView import CheckBoxView



class JustCalcView:

    def __init__(self) -> None:
        self.listeners: list[Any]= []
        self.style = Style()
        self.window = tk.Tk()
        self.ttk_style = ttk.Style()
        self.ttk_style.theme_use('clam')

        self.setup_window()
        self.setup_widgets()
        self.setup_layout()

    
    def add_listener(self, listener):
        print("JustCalcView add listener")
        self.listeners.append(listener)

   
    def on_change(self, event=None):
        print("JustCalcView on_changed")
        
        for listener in self.listeners:
            result = listener(self.expression_text.get_text(), self.checkbox.is_checked())
            self.answer_text.set_text(result)
        
        self.sync_scroll_positions()
        self.delayed_scrollbar_check()


    def setup_window(self) -> None:
        self.window.title("JustCalc")
        self.window.geometry("600x200")
        self.window.resizable(True, True)
        
        # Apply dark theme to main window
        self.window.configure(bg=self.style.dark_color)
        

    def setup_widgets(self) -> None:
        self.expression_text = TextBoxView(self.window, self.style)
        self.answer_text = TextBoxView(self.window, self.style)
        self.scrollbar = ScrollBarView(self.window, self.style)
        self.checkbox = CheckBoxView(self.window, self.style)

        # Info label below editors
        self.info_label = tk.Label(
            self.window,
            text="""Type expressions on the left. Results appear on the right. 
Supports trig functions like sin(x), cos(x), variables x=5, x^2 and more.""",
            bg=self.style.dark_color,
            fg=self.style.light_color,
            anchor='w',
            justify='left'
        )

        self.checkbox.add_listener(self.on_change)

    

    def setup_layout(self) -> None:
         # Make columns expand
        self.window.grid_columnconfigure(0, weight=8, minsize=200)
        self.window.grid_columnconfigure(1, weight=8, minsize=200)  
        self.window.grid_columnconfigure(2, weight=0)  
        self.window.grid_rowconfigure(0, weight=1)


        self.expression_text.get_view().grid(row=0, column=0, sticky="nsew", padx = (self.style.padding, self.style.padding), pady = self.style.padding)
        self.answer_text.get_view().grid(row=0, column=1, sticky="nsew", padx = (0,self.style.padding), pady = self.style.padding)
        self.scrollbar.get_view().grid(row=0, column=2, sticky="ns")
        self.checkbox.get_view().grid(row=1, column=0, sticky="w", padx=self.style.padding, pady=(0, self.style.padding))
        self.info_label.grid(row=2, column=0, columnspan=3, sticky="ew", padx=self.style.padding, pady=(0, self.style.padding))


        # Function to sync scrolling
        def sync_scroll(*args) -> None:
            # Update scrollbar position
            self.scrollbar.get_view().set(*args)
            

        def scroll_both(*args) -> None:
            # Synchronize both text widgets when scrollbar is moved
            self.expression_text.get_view().yview(*args)
            self.answer_text.get_view().yview(*args)
            self.update_scrollbar_visibility()

        # Connect scrollbar to both texts
        self.scrollbar.get_view().config(command=scroll_both)
        self.expression_text.get_view().config(yscrollcommand=sync_scroll)
        self.answer_text.get_view().config(yscrollcommand=sync_scroll)

        # Bind the evaluate function to key release
        self.expression_text.get_view().bind('<KeyRelease>', self.on_change)
        self.checkbox.add_listener(self.on_change)

        # Bind window resize to update scrollbar visibility
        self.window.bind('<Configure>', self.delayed_scrollbar_check)


        def _select_expression_initial() -> None:
            self.expression_text.get_view().focus_set()
            #self.expression_text.tag_add("sel", "1.0", "end-1c")
            #self.expression_text.mark_set("insert", "end-1c")

        self.window.after(0, _select_expression_initial)



    def sync_scroll_positions(self) -> None:
        """Synchronize the scroll positions of both text widgets."""
        try:
            # Get current scroll position from expression text
            current_pos = self.expression_text.get_view().yview()
            # Apply same position to answer text
            self.answer_text.get_view().yview_moveto(current_pos[0])
        except Exception:
            pass  # Ignore any scroll-related errors



    def needs_scrollbar(self, text: tk.Text) -> bool:
        """Checks vertical size"""
        font = tkFont.Font(font=text['font'])
        font_height = font.metrics("linespace")
        #print("Font height:", font_height)

        visible_lines = text.winfo_height() // font_height
        total_lines = int(text.index("end-1c").split(".")[0])

        if total_lines > visible_lines:
            #print("Vertical overflow detected")
            return True
        return False



    def update_scrollbar_visibility(self, event=None) -> None:
        if self.needs_scrollbar(self.expression_text.get_view()):
            self.scrollbar.get_view().grid(row=0, column=2, sticky="ns")
        else:
            self.scrollbar.get_view().grid_forget()
    

    def delayed_scrollbar_check(self, event=None) -> None:
        self.window.after(100, self.update_scrollbar_visibility)
    
    
    def get_view(self) -> Any:
        return self.window


    def run(self):
        self.window.mainloop()

        
        
