# theme.py
from tkinter import ttk, colorchooser

class Theme:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.set_default_theme()

    def set_default_theme(self):
        # Default colors
        self.set_theme("white", "black", "white", "black")

    def open_color_picker(self):
        # Open color pickers for foreground and background
        entry_fg = colorchooser.askcolor(title="Pick Entry Foreground Color")[1]
        entry_bg = colorchooser.askcolor(title="Pick Entry Background Color")[1]
        text_fg = colorchooser.askcolor(title="Pick Text Foreground Color")[1]
        text_bg = colorchooser.askcolor(title="Pick Text Background Color")[1]
        
        # Ensure all color values are valid (and not None)
        if entry_fg and entry_bg and text_fg and text_bg:
            self.set_theme(entry_bg, entry_fg, text_bg, text_fg)

    def set_theme(self, entry_bg, entry_fg, text_bg, text_fg):
        self.entry_background = entry_bg
        self.entry_foreground = entry_fg
        self.text_background = text_bg
        self.text_foreground = text_fg
        
        # Apply the chosen colors to the root
        self.apply()

    def apply(self):
        # Update ttk styles
        self.style.configure('TLabel', background=self.root.cget('bg'), foreground=self.entry_foreground) 
        self.style.configure('TButton', background=self.root.cget('bg'))
        self.style.configure('TFrame', background=self.root.cget('bg'))

    def apply_to_widgets(self, entry_widget, text_widget):
        entry_widget.config(background=self.entry_background, foreground=self.entry_foreground, insertbackground=self.entry_foreground)
        text_widget.config(background=self.text_background, foreground=self.text_foreground, insertbackground=self.text_foreground)