import os
import glob
import pandas as pd
import tkinter as tk
from ui import UI


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_attributes("-zoomed", True)
        self.ui = UI(self)
        self.report = self.load_last_report()
        from_date = self.report["Date"].min()
        to_date = self.report["Date"].max()
        self.title(
            f"FUEL - from {from_date.day}/{from_date.month}/{from_date.year} \
             to {to_date.day}/{to_date.month}/{to_date.year}"
        )
        self.load_items()

    def load_last_report(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, "Data")
            reports = glob.glob(os.path.join(data_dir, "*.xlsx"))
            last_report = max(reports, key=os.path.getctime)
            path_to_last_report = os.path.join(data_dir, last_report)
            report = pd.read_excel(path_to_last_report)
            return report
        except Exception as e:
            print("Exception:", e)
            self.ui.status_label.config(
                text="Something went wrong when loading your data"
            )
            return None

    def quit_app(self):
        self.destroy()

    def load_items(self):
        self.ui.status_label.config(text="")
        self.ui.treeview.delete(*self.ui.treeview.get_children())
        self.ui.treeview["columns"] = ("#", "Item", "Quantity")
        self.ui.treeview.column("#", anchor=tk.CENTER, stretch=0, width=50)
        self.ui.treeview.column("Item", anchor=tk.CENTER)
        self.ui.treeview.column("Quantity", anchor=tk.CENTER)

        self.ui.treeview.heading("#", text="#", anchor=tk.CENTER)
        self.ui.treeview.heading("Item", text="Item", anchor=tk.CENTER)
        self.ui.treeview.heading("Quantity", text="Quantity", anchor=tk.CENTER)

        fuel_group = self.report.groupby("Article")
        fuel_group_sums = fuel_group["Quantity"].sum()

        for i, group in enumerate(fuel_group_sums.items(), start=1):
            item, quantity = group
            if i % 2:
                self.ui.treeview.insert(
                    "", "end", values=(str(i), item, quantity), tag="font"
                )
            else:
                self.ui.treeview.insert(
                    "",
                    "end",
                    values=(str(i), item, quantity),
                    tag=("even", "font"),
                )
        self.ui.treeview.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.ui.items_button.config(command=self.load_items)
        self.ui.category_button.config(text="Category", state="disabled")
        self.ui.detail_button.config(text="Detail", state="disabled")

    def on_item_selected(self, event=None, item_values=None):
        if not item_values:
            selected_item = self.ui.treeview.selection()
            item_values = self.ui.treeview.item(selected_item)

        _, category, quantity = item_values["values"]
        self.ui.status_label.config(text=f"Total quantity for {category}: {quantity}")

        filt = self.report["Article"] == category
        cars_group = self.report[filt].groupby("Registration")
        cars_group_sums = cars_group["Quantity"].sum()

        self.ui.treeview.unbind("<<TreeviewSelect>>")
        self.ui.treeview.delete(*self.ui.treeview.get_children())

        for i, group in enumerate(cars_group_sums.items(), start=1):
            item, quantity = group
            if i % 2:
                self.ui.treeview.insert(
                    "", "end", values=(str(i), item, quantity), tag="font"
                )
            else:
                self.ui.treeview.insert(
                    "",
                    "end",
                    values=(str(i), item, quantity),
                    tag=("even", "font"),
                )
        self.ui.treeview.bind("<<TreeviewSelect>>", self.on_car_selected)
        self.ui.category_button.config(
            command=lambda: self.on_item_selected(item_values=item_values)
        )
        self.ui.category_button.config(state="active", text=category)
        self.ui.detail_button.config(text="Detail", state="disabled")

    def on_car_selected(self, event=None, car=None):
        selected_item = self.ui.treeview.selection()
        if selected_item:
            item_values = self.ui.treeview.item(selected_item)
            _, car, quantity = item_values["values"]
            filt = self.report["Registration"] == car
            group = self.report[filt][["Date", "Quantity", "Net total", "Gross total"]]
            group["Date"] = group["Date"].dt.strftime("%d/%m/%Y")

            self.ui.status_label.config(
                text=f"Total quantity for car {car}: {quantity}"
            )

            self.ui.detail_button.config(state="active", text=car)

            self.ui.treeview.delete(*self.ui.treeview.get_children())
            self.ui.treeview["columns"] = (
                "#",
                "Date",
                "Quantity",
                "Net total",
                "Gross total",
            )
            self.ui.treeview.column("#", anchor=tk.CENTER, stretch=0, width=50)
            self.ui.treeview.column("Date", anchor=tk.CENTER)
            self.ui.treeview.column("Quantity", anchor=tk.CENTER)
            self.ui.treeview.column("Net total", anchor=tk.CENTER)
            self.ui.treeview.column("Gross total", anchor=tk.CENTER)

            self.ui.treeview.heading("#", text="#", anchor=tk.CENTER)
            self.ui.treeview.heading("Date", text="Date", anchor=tk.CENTER)
            self.ui.treeview.heading("Quantity", text="Quantity", anchor=tk.CENTER)
            self.ui.treeview.heading("Net total", text="Net total", anchor=tk.CENTER)
            self.ui.treeview.heading(
                "Gross total", text="Gross total", anchor=tk.CENTER
            )

            self.ui.treeview.unbind("<<TreeviewSelect>>")

            for i, value in enumerate(group.values, start=1):
                if i % 2:
                    self.ui.treeview.insert(
                        "",
                        "end",
                        values=(
                            str(i),
                            value[0],
                            value[1],
                            value[2],
                            value[3],
                        ),
                        tag="font",
                    )
                else:
                    self.ui.treeview.insert(
                        "",
                        "end",
                        values=(
                            str(i),
                            value[0],
                            value[1],
                            value[2],
                            value[3],
                        ),
                        tag=("even", "font"),
                    )


if __name__ == "__main__":
    app = App()
    app.mainloop()
