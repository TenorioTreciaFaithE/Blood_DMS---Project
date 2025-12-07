import tkinter as tk
from tkinter import ttk


class BasePage(ttk.Frame):
    def __init__(self, parent: tk.Widget, title: str, subtitle: str | None = None) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self, highlightthickness=0, background="#f5f5f5")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding=10, style="Content.TFrame")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        
        self.scrollable_frame.columnconfigure(0, weight=1)
        
        header = ttk.Label(self.scrollable_frame, text=title, style="Header.TLabel")
        header.grid(row=0, column=0, sticky="w")

        if subtitle:
            subtitle_label = ttk.Label(self.scrollable_frame, text=subtitle, style="Subtle.TLabel")
            subtitle_label.grid(row=1, column=0, sticky="w", pady=(2, 10))
            self.body_row = 2
        else:
            self.body_row = 1
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def _on_canvas_configure(self, event=None):
        if event:
            canvas_width = event.width
        else:
            canvas_width = self.canvas.winfo_width()
        canvas_items = self.canvas.find_all()
        if canvas_items:
            self.canvas.itemconfig(canvas_items[0], width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_card(self, parent: tk.Widget, title: str, subtitle: str | None = None) -> ttk.Frame:
        card = ttk.Frame(parent, padding=10, style="Card.TFrame")
        card.columnconfigure(0, weight=1)
        heading = ttk.Label(card, text=title, style="CardHeading.TLabel")
        heading.grid(row=0, column=0, sticky="w", pady=(0, 2))
        if subtitle:
            sub = ttk.Label(card, text=subtitle, style="CardSubtitle.TLabel")
            sub.grid(row=1, column=0, sticky="w", pady=(0, 10))
        return card

