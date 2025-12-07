import tkinter as tk
from tkinter import ttk

from pages.dashboard import DashboardPage
from pages.donor_management import DonorManagementPage
from pages.blood_inventory import BloodInventoryPage
from pages.donation_management import DonationManagementPage
from pages.request_management import RequestManagementPage


def center_window(window, width=None, height=None):
    window.update_idletasks()
    
    if width is None or height is None:
        width = window.winfo_width()
        height = window.winfo_height()
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")


class BloodDonationSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blood Donation Management System")
        self.minsize(1366, 768)
        self.maxsize(1366, 768)

        self.configure(background="#f5f5f5")
        
        center_window(self, 1366, 768)

        self.style = ttk.Style(self)
        self._setup_styles()

        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=180)
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self, style="Content.TFrame")
        self.content.pack(side="right", expand=True, fill="both")

        self.logo_label = ttk.Label(
            self.sidebar,
            text="BLOOD\nDONATION\nMANAGEMENT",
            style="SidebarHeading.TLabel",
            justify="left",
        )
        self.logo_label.pack(anchor="w", padx=12, pady=(12, 16))

        self.nav_buttons: dict[str, ttk.Button] = {}
        self.pages: dict[str, tk.Frame] = {}

        navigation_items = [
            ("Dashboard", DashboardPage),
            ("Donor Management", DonorManagementPage),
            ("Blood Inventory", BloodInventoryPage),
            ("Donation Management", DonationManagementPage),
            ("Request Management", RequestManagementPage),
        ]

        for text, page_class in navigation_items:
            button = ttk.Button(
                self.sidebar,
                text=text,
                style="Sidebar.TButton",
                command=lambda name=text, cls=page_class: self.show_page(name, cls),
            )
            button.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[text] = button

        ttk.Separator(self.sidebar).pack(fill="x", padx=12, pady=12)

        footer = ttk.Label(
            self.sidebar,
            text="Blood Donation\nManagement System",
            style="SidebarFooter.TLabel",
            justify="left",
        )
        footer.pack(anchor="w", padx=12, pady=(0, 8))

        self.show_page("Dashboard", DashboardPage)

    def _setup_styles(self) -> None:
        self.style.theme_use("clam")

        # Red color scheme for blood donation system
        self.style.configure("Sidebar.TFrame", background="#8B0000")  # Dark red
        self.style.configure("Content.TFrame", background="#eeeeee")
        self.style.configure("SidebarHeading.TLabel", font=("Segoe UI", 14, "bold"), foreground="white", background="#8B0000")
        self.style.configure("SidebarFooter.TLabel", font=("Segoe UI", 8), foreground="#e0e0e0", background="#8B0000")
        self.style.configure("Sidebar.TButton", font=("Segoe UI", 9, "bold"), anchor="w", padding=(10, 8))
        self.style.map(
            "Sidebar.TButton",
            background=[("pressed", "#5C0000"), ("active", "#A00000"), ("!disabled", "#B22222")],
            foreground=[("pressed", "white"), ("!disabled", "white")],
        )
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("CardHeading.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#333333")
        self.style.configure("CardSubtitle.TLabel", font=("Segoe UI", 9), background="#ffffff", foreground="#555555")
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#8B0000", background="#eeeeee")
        self.style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"), foreground="#555555", background="#eeeeee")
        self.style.configure("Subtle.TLabel", font=("Segoe UI", 9), foreground="#888888", background="#eeeeee")
        self.style.configure("Label.TLabel", font=("Segoe UI", 9), foreground="#555555", background="#eeeeee")
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        self.style.map(
            "Accent.TButton",
            background=[("active", "#A00000"), ("!disabled", "#8B0000")],
            foreground=[("!disabled", "white")],
        )
        self.style.configure("Outline.TButton", font=("Segoe UI", 9, "bold"))
        self.style.map(
            "Outline.TButton",
            background=[("active", "#e8e8e8"), ("!disabled", "#eeeeee")],
            foreground=[("!disabled", "#555555")],
            bordercolor=[("active", "#d0d0d0"), ("!disabled", "#d0d0d0")],
        )
        self.style.configure("TFrame", background="#eeeeee")
        self.style.configure("Treeview", background="#ffffff", foreground="#333333", fieldbackground="#ffffff", rowheight=24)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#8B0000", foreground="white")
        self.style.configure("TEntry", fieldbackground="#ffffff", foreground="#333333", bordercolor="#d0d0d0", lightcolor="#d0d0d0", darkcolor="#d0d0d0")
        self.style.map("TEntry", bordercolor=[("focus", "#8B0000"), ("!focus", "#d0d0d0")])
        self.style.configure("TCombobox", fieldbackground="#ffffff", foreground="#333333", bordercolor="#d0d0d0", lightcolor="#d0d0d0", darkcolor="#d0d0d0")
        self.style.map("TCombobox", bordercolor=[("focus", "#8B0000"), ("!focus", "#d0d0d0")])
        self.style.configure("TRadiobutton", background="#eeeeee", foreground="#555555")
        self.style.configure("TLabelFrame", background="#ffffff", foreground="#555555")
        self.style.configure("TLabelFrame.Label", background="#ffffff", foreground="#555555", font=("Segoe UI", 10, "bold"))

    def show_page(self, name: str, page_class: type[tk.Frame]) -> None:
        for text, button in self.nav_buttons.items():
            if text == name:
                button.state(["pressed"])
            else:
                button.state(["!pressed"])

        for child in self.content.winfo_children():
            child.destroy()

        page = page_class(self.content)
        page.pack(expand=True, fill="both", padx=10, pady=10)
        self.pages[name] = page


if __name__ == "__main__":
    app = BloodDonationSystem()
    app.mainloop()