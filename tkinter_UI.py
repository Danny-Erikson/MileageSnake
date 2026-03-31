import tkinter as tk
from tkinter import ttk

#* Module Imports
from modules.UI_elements.car_manager import show_car_manager
from modules.UI_elements.mileage_screen import show_mileage_screen


class Service_UI:
    def __init__(self, master, db):
        self.master = master
        master.title("Mileage Snake")
        master.geometry("600x500")
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.int_vcmd = master.register(self._only_numbers)
        self.float_vcmd = master.register(self._only_floats)
        
        self.db = db
        
        #Call to Info used on multiple screens
        self.cars = self.db.get_all_cars()
        
        #Runtime
        self._show_main_screen()


    #* Builders


    def _show_main_screen(self):
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        
        title_label = tk.Label(self.master, text="Service Logger", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=25)
        
        mileage_button = ttk.Button(self.master, text="Enter Mileage", command=lambda: show_mileage_screen(self))
        mileage_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        service_button = ttk.Button(self.master, text="Service Entering", command="")
        service_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        man_cars_button = ttk.Button(self.master, text="Manage cars", command=lambda: show_car_manager(self))
        man_cars_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        man_services_button = ttk.Button(self.master, text="Manage recurring services")
        man_services_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        gen_report = ttk.Button(self.master, text="Generate Service Report")
        gen_report.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


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

    def _only_floats(self, new_value):
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False
