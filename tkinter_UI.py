import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt

#* Module Imports
from modules.UI_elements.car_manager import show_car_manager


class Service_UI:
    def __init__(self, master, db):
        self.master = master
        master.title("Mileage Snake")
        master.geometry("600x500")
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.vcmd = master.register(self._only_numbers)
        
        self.db = db
        
        #Runtime
        self._show_main_screen()


    #* Builders

    def _create_shared_widgets(self):
        """
        Used to build the UI elements for the car selector, mileage, and date entry
        """
        #TODO: Add a MPG Area, This make the _create_shared useable
        #TODO: Add number only for the mileage area
        self.car_var = tk.StringVar()
        self.mileage_var = tk.IntVar()
        self.date_var = tk.StringVar()

        self.cars = self.db.get_all_cars()

        car_label = ttk.Label(self.master, text="Car: ")
        car_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.car_combo = ttk.Combobox(self.master, textvariable=self.car_var, state="readonly")
        self.car_combo["values"] = [f"{c['Year']} {c['Make']} {c['Model']}" for c in self.cars]
        self.car_var.set(self.car_combo["values"][0])
        self.car_combo.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        mileage_label = ttk.Label(self.master, text="Mileage:")
        mileage_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        mileage_entry = ttk.Entry(self.master, textvariable=self.mileage_var, validate="key", validatecommand=(self.vcmd, "%P"))
        mileage_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        mileage_date_label = ttk.Label(self.master, text="Date of reading:")
        mileage_date_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)

        mileage_date = ttk.Entry(self.master, textvariable=self.date_var)
        self.date_var.set(value=dt.date.today())
        mileage_date.grid(row=3, column=1, sticky="w", padx=10, pady=10)


    def _show_main_screen(self):
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        
        title_label = tk.Label(self.master, text="Service Logger", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=25)
        
        mileage_button = ttk.Button(self.master, text="Enter Mileage", command=self._show_mileage_screen)
        mileage_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        service_button = ttk.Button(self.master, text="Service Entering", command="")
        service_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        man_cars_button = ttk.Button(self.master, text="Manage cars", command=lambda: show_car_manager(self))
        man_cars_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        man_services_button = ttk.Button(self.master, text="Manage recurring services")
        man_services_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        gen_report = ttk.Button(self.master, text="Generate Service Report")
        gen_report.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


    #* Mileage
    def _show_mileage_screen(self):
        #* Initialize Frame & Call DB
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        title_label = tk.Label(self.master, text="Enter Mileage", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=25)

        self._create_shared_widgets()

        mile_submit = ttk.Button(self.master, text="Enter Mileage", command=self._add_mileage)
        mile_submit.grid(row=4, columnspan=2, padx=10, pady=10)

        back_button = ttk.Button(self.master, text="Go Back", command=self._show_main_screen)
        back_button.grid(row=5, columnspan=2, padx=10, pady=10)

    #* Mileage Helper
    def _add_mileage(self):
        self.db.add_mileage(self.cars[self.car_combo.current()]["CarID"],
                            self.mileage_var.get(),
                            self.date_var.get())
        
        messagebox.showinfo("Mileage Entered", "Your Mileage has been entered")
        
        self._show_main_screen()


    #* Helper functions

    def _on_close(self):
        self.master.destroy()

    def _clear_frame(self):
        #clears elements
        for widget in self.master.winfo_children():
            widget.destroy()
        # Reset column/row weight
        for i in range(10):
            self.master.columnconfigure(i, weight=0)
            self.master.rowconfigure(i, weight=0)

    def _only_numbers(self, new_value):
        return new_value.isdigit() or new_value == ""