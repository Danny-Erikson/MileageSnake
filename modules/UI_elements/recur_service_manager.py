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

    ui.service = ui.db.get_all_recurring_service()
    
    #* Top of screen
    title_label = tk.Label(ui.master, text="Recurring Services", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=5, pady=TITLE_Y)
    
    ui.car_combo = ttk.Combobox(ui.master, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][0])
    ui.car_combo.grid(row=1, column=0, columnspan=5, padx=ENTRY_X, pady=ENTRY_Y)

    service_label = tk.Label(ui.master, text="Service")
    service_label.grid(row=2, column=1, sticky="ew")
    service_in_miles_label = tk.Label(ui.master, text="Service Interval (Miles)")
    service_in_miles_label.grid(row=2, column=2, sticky="ew")
    service_in_days_label = tk.Label(ui.master, text="Service Interval (Days)")
    service_in_days_label.grid(row=2, column=3, sticky="ew")


    #* Table Builder 
    row_count = 3
    #FIXME: We need to filter by Car ID 
    #FIXME: also look into scoll test
    for service in ui.service:
        edit_button = tk.Button(ui.master, text="🖉", command=lambda serviceID=service["ServiceId"]: show_service_form(ui, editing=True, serviceID=serviceID))
        edit_button.grid(row=row_count, column=0, sticky="ew")
        service_name = tk.Label(ui.master, text=f"{service["Name"]}")
        service_name.grid(row=row_count, column=1, sticky="ew")
        service_in_miles = tk.Label(ui.master, text=f"{service["DueMileage"]}")
        service_in_miles.grid(row=row_count, column=2, sticky="ew")
        service_in_days = tk.Label(ui.master, text=f"{service["DueDays"]}")
        service_in_days.grid(row=row_count, column=3, sticky="ew")
        remove_car_button = tk.Button(ui.master, text="Remove Car", command=lambda serviceID=service["ServiceId"]: remove_service(ui, serviceID=serviceID))
        remove_car_button.grid(row=row_count, column=4, sticky="ew")
        row_count += 1

def show_service_form(self, serviceID, editing=False):
    pass

def remove_service(self, serviceID):
    pass