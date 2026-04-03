import tkinter as tk
from tkinter import ttk, messagebox

from ui_padding import *

#NOTE: self.cars is called at launch in tkinker_UI

def show_recur_service_manager(ui):
    #* Initialize Frame
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    ui.master.columnconfigure(2, weight=1)
    ui.master.columnconfigure(3, weight=1)
    ui.master.columnconfigure(4, weight=1)
    
    ui.car_var = tk.StringVar()
    
    #* Top of screen
    title_label = tk.Label(ui.master, text="Recurring Services", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=5, pady=TITLE_Y)
    
    ui.car_combo = ttk.Combobox(ui.master, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][0])
    ui.car_combo.bind("<<ComboboxSelected>>", lambda e: on_car_change(ui))
    ui.car_combo.grid(row=1, column=0, columnspan=5, padx=ENTRY_X, pady=ENTRY_Y)
    
    #* Service Table
    ui.service_table = tk.Frame(ui.master)
    ui.service_table.grid(row=2, column=0, columnspan=5, sticky="ew")
    
    ui.service_table.columnconfigure(0, weight=1)
    ui.service_table.columnconfigure(1, weight=1)
    ui.service_table.columnconfigure(2, weight=1)
    ui.service_table.columnconfigure(3, weight=1)
    ui.service_table.columnconfigure(4, weight=1)
    
    tk.Label(ui.service_table, text="").grid(row=0, column=0, sticky="ew")
    tk.Label(ui.service_table, text="Service").grid(row=0, column=1, sticky="ew")
    tk.Label(ui.service_table, text="Service Interval (Miles)").grid(row=0, column=2, sticky="ew")
    tk.Label(ui.service_table, text="Service Interval (Every)").grid(row=0, column=3, sticky="ew")
    tk.Label(ui.service_table, text="").grid(row=0, column=4, sticky="ew")
    
    on_car_change(ui)

def on_car_change(ui):
    for widget in ui.service_table.winfo_children():
        info = widget.grid_info()
        if int(info["row"]) > 0:   # keep header row
            widget.destroy()
    
    index = ui.car_combo.current()
    services = ui.db.get_recurring_services_by_carID(ui.cars[index]["CarID"])
    
    
    row_count = 1
    for service in services:
        edit_button = tk.Button(
            ui.service_table,
            text="🖉",
            command=lambda serviceID=service["ServiceId"]: show_service_form(ui, editing=True, serviceID=serviceID)
        )
        edit_button.grid(row=row_count, column=0, sticky="ew")
        
        service_name = tk.Label(ui.service_table, text=service["Name"])
        service_name.grid(row=row_count, column=1, sticky="ew")
        
        service_in_miles = tk.Label(ui.service_table, text=service["DueMileage"])
        service_in_miles.grid(row=row_count, column=2, sticky="ew")
        
        service_in_days = tk.Label(ui.service_table, text=service["DueDays"])
        service_in_days.grid(row=row_count, column=3, sticky="ew")
        
        remove_service_button = tk.Button(
            ui.service_table,
            text="Remove Service",
            command=lambda serviceID=service["ServiceId"]: remove_service(ui, serviceID=serviceID)
        )
        remove_service_button.grid(row=row_count, column=4, sticky="ew")
        
        row_count += 1

def show_service_form(self, serviceID, editing=False):
    pass

def remove_service(self, serviceID):
    pass