import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from typing import Any

from Style import Style



class CheckBoxView:
    
    def __init__(self, parent: Any, style: Style) -> None:
        print("CheckBoxView __init__")

        self.checked = tk.BooleanVar(value=True)

        self.listeners: list[Any] = []

        # Angle mode toggle
        def on_toggle() -> None:
            self.on_change(self.checked.get())
         

        self.view = tk.Checkbutton(
            parent,
            text="Use Degrees",
            variable=self.checked,
            onvalue=True,
            offvalue=False,
            bg=style.dark_color,
            fg=style.text_color,
            activebackground=style.dark_color,
            activeforeground=style.text_color,
            selectcolor=style.dark_color,
            highlightthickness=0,
            command=on_toggle
        )


    def add_listener(self, listener):
        print("CheckBoxView add listener")
        self.listeners.append(listener)


    def on_change(self, new_value: bool):
        print(f"CheckBoxView on_changed {new_value}")
        #self.checked.set(new_value)

        for listener in self.listeners:
            listener()


    def is_checked(self) -> bool:
        print(f"CheckBoxView get() {self.checked.get() = }")
        return self.checked.get()

        

    def get_view(self) -> Any:
        return self.view
