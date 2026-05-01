import tkinter as tk
from tkinter import ttk, messagebox

import datetime as dt

from ui_padding import *

#* Module Imports
from modules.UI_elements.mileage_screen import show_mileage_screen
from modules.UI_elements.service_screen import show_service_screen
from modules.UI_elements.car_manager import show_car_manager
from modules.UI_elements.recur_service_manager import show_recur_service_manager
from modules.UI_elements.default_services_editor import show_default_services_editor


class Service_UI:
    def __init__(self, master, db):
        self.master = master
        master.title("Mileage Snake")
        master.geometry("1080x1080")
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.int_vcmd = master.register(self._only_numbers)
        self.float_vcmd = master.register(self._only_floats)
        
        self.db = db
        
        self.cars = self.db.get_all_cars()
        
        self.car_index = 0 
        
        #Runtime
        self._show_main_screen()
    
    #* Builders
    def _show_main_screen(self):
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        
        title_label = tk.Label(self.master, text="Service Logger", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
        
        mileage_button = ttk.Button(self.master, text="Enter Mileage", command=lambda: show_mileage_screen(self))
        mileage_button.grid(row=1, column=0, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
        
        service_button = ttk.Button(self.master, text="Service Entering", command=lambda: show_service_screen(self))
        service_button.grid(row=1, column=1, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
        
        gen_report = ttk.Button(self.master, text="Generate Reports")
        gen_report.grid(row=2, column=0, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
        
        advanced_button  = ttk.Button(self.master, text="Advanced Area", command=self.show_advanced_area)
        advanced_button.grid(row=2, column=1, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
    
    def show_advanced_area(self):
        #* Initialize Frame
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        
        #* Top of the Screen
        title_label = tk.Label(self.master, text="Advanced", font=("Arial", 16))
        title_label.grid(row=0, columnspan=2, pady=TITLE_Y)
        
        #* Middle of the screen
        man_cars_button = ttk.Button(self.master, text="Manage cars", command=lambda: show_car_manager(self))
        man_cars_button.grid(row=1, column=0, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
        
        man_services_button = ttk.Button(self.master, text="Manage recurring services", command=lambda: show_recur_service_manager(self))
        man_services_button.grid(row=1, column=1, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
        
        edit_re_services = tk.Button(self.master, text="Edit Default Services", command=lambda: show_default_services_editor(self))
        edit_re_services.grid(row=2, column= 1, padx=BUTTON_X, pady=BUTTON_Y, sticky="ew")
        
        #* Bottom of the screen
        go_back = tk.Button(self.master, text="Go Back", command=self._show_main_screen)
        go_back.grid(row=3, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
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
    
    def is_valid_date(self, date_str):
        try:
            dt.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def no_id_reroute(self):
        messagebox.showerror("No Cars Error", "Whoops!\nLooks like there are no cars in the database, we'll reroute you to the car manager to enter one")
        show_car_manager(self)
