import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont


class UI:
    def __init__(self, root):
        root.rowconfigure(0, weight=0)  # Breadcrumbs row
        root.rowconfigure(1, weight=1)  # Main row
        root.rowconfigure(2, weight=0)  # Status line row
        root.columnconfigure(0, weight=1)
        menu = self.create_menu(root)
        root.config(menu=menu)
        self.breadcrumbs_frame = tk.Frame(root)
        self.breadcrumbs_frame.grid(column=0, row=0, sticky="w")
        self.main_frame = tk.Frame(root)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.grid(column=0, row=1, sticky="nswe")
        self.status_frame = tk.Frame(root)
        self.status_frame.grid(column=0, row=2, sticky="w")
        self.create_breadcrumbs()
        self.create_main_content()
        self.create_status_bar()

    def create_menu(self, root):
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=root.quit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=self.create_about)
        menu_bar.add_cascade(label="Help", menu=about_menu)
        return menu_bar

    def create_breadcrumbs(self):
        self.items_button = tk.Button(master=self.breadcrumbs_frame, text="Items", bd=0)
        self.items_button.grid(column=0, row=0, padx=5, pady=5)
        tk.Label(master=self.breadcrumbs_frame, text=">").grid(column=1, row=0)
        self.category_button = tk.Button(master=self.breadcrumbs_frame, bd=0)
        self.category_button.grid(column=2, row=0)
        tk.Label(master=self.breadcrumbs_frame, text=">").grid(column=3, row=0)
        self.detail_button = tk.Button(master=self.breadcrumbs_frame, bd=0)
        self.detail_button.grid(column=4, row=0)

    def create_main_content(self):
        self.treeview = ttk.Treeview(master=self.main_frame, show="headings")
        self.treeview.tag_configure("even", background="#D3D3D3")
        self.treeview.tag_configure("font", font=tk.font.Font(size=12))
        self.treeview.configure
        scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.treeview.yview
        )
        scrollbar.grid(column=1, row=0, sticky="ns")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        nametofont("TkHeadingFont").configure(weight="bold", size=12)
        self.treeview.grid(row=0, column=0, sticky="nswe")

    def create_status_bar(self):
        self.status_label = tk.Label(master=self.status_frame)
        self.status_label.grid(column=0, row=0, padx=5)

    def create_about(self):
        about_window = tk.Toplevel()
        about_window.title("FUEL")
        about_window.geometry("300x200")  # Set size of the window
        about_window.grid_columnconfigure(0, weight=1)  # Expand column for centering

        title_label = tk.Label(
            about_window,
            text="FUEL",
            font=("Arial", 17, "bold"),
        )
        title_label.grid(column=0, row=0, pady=10)

        version_label = tk.Label(about_window, text="Version: 1.0")
        version_label.grid(column=0, row=1)

        author_label = tk.Label(about_window, text="Author: Sławomir Kwiatkowski")
        author_label.grid(column=0, row=2)

        date_label = tk.Label(about_window, text="date: 2024/12/15")
        date_label.grid(column=0, row=3)

        close_button = tk.Button(
            about_window, text="Close", command=about_window.destroy
        )
        close_button.grid(column=0, row=4, pady=20)
