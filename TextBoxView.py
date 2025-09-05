from typing import Any
from Style import Style
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont



class TextBoxView:

    def __init__(self, parent: Any, style: Style) -> None:
        self.text_lines: list[str]= []
        
        self.view = tk.Text(
            parent,
            height=5,
            width=150,
            bg=style.medium_color,
            fg=style.text_color,
            highlightthickness=style.border_thickness,
            highlightcolor=style.light_accent_color,
            highlightbackground=style.light_color,
            insertbackground=style.text_color,
            selectbackground=style.light_color,
            selectforeground=style.dark_color,
            relief='flat',
            borderwidth=0,
            font=(style.font, style.text_size)
        )

        self.view.tag_configure('sel')


    def set_text(self, text_lines: list[str]) -> None:
        # Clear output
        self.view.config(state='normal')
        self.view.delete("1.0", tk.END)

        self.text_lines = text_lines
        self.view.insert(tk.END, '\n'.join(self.text_lines))
        #self.view.config(state='disabled')


    def get_text(self) -> list[str]:
        # Get all lines from input
        input_lines = self.view.get("1.0", tk.END).split('\n')
        # Remove the last empty line that tk.END creates
        if input_lines and input_lines[-1] == '':
            input_lines.pop()

        return input_lines


    def format_text_for_view(self) -> list[str]:
        #TODO chop length of lines to fit in view
        return []


    def get_view(self) -> Any:
        return self.view