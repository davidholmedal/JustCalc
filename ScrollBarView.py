import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from typing import Any

from Style import Style



class ScrollBarView:

    def __init__(self, parent: Any, style: Style) -> None:
        
        ttk.Style().configure("Custom.Vertical.TScrollbar",
            gripcount=0,
            background = style.light_color,   # the thumb color
            darkcolor = style.medium_color,    # shadow
            lightcolor = style.medium_color,   # highlight
            troughcolor = style.dark_color,      # track color
            bordercolor = style.black,  
            arrowcolor = style.text_color     
        )

        self.view = ttk.Scrollbar(
            #self.frame_right, 
            parent, 
            style="Custom.Vertical.TScrollbar"
        )


    def set_scroll_pos(self, percentage: float = 0.0) -> None:
        pass
        

    def get_scroll_pos(self, percentage: float = 0.0) -> None:
        pass


    def get_view(self) -> Any:
        return self.view