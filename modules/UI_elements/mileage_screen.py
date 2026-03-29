import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt

from ui_padding import *


#* Mileage

def show_mileage_screen(ui):
    #* Initialize Frame & Call DB
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    
    ui.car_var = tk.StringVar()
    ui.mileage_var = tk.IntVar()
    ui.date_var = tk.StringVar()
    
    title_label = tk.Label(ui.master, text="Enter Mileage", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
    
    ui.cars = ui.db.get_all_cars()
    
    #* Mileage Area
    car_label = ttk.Label(ui.master, text="Car: ")
    car_label.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.car_combo = ttk.Combobox(ui.master, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][0])
    ui.car_combo.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_label = ttk.Label(ui.master, text="Mileage:")
    mileage_label.grid(row=2, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_entry = ttk.Entry(ui.master, textvariable=ui.mileage_var, validate="key", validatecommand=(ui.int_vcmd, "%P"))
    mileage_entry.grid(row=2, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_date_label = ttk.Label(ui.master, text="Date of reading:")
    mileage_date_label.grid(row=3, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_date = ttk.Entry(ui.master, textvariable=ui.date_var)
    ui.date_var.set(value=dt.date.today())
    mileage_date.grid(row=3, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    #* Mileage Area
    #FIXME: The Checkbox doesn't disable the fields
    #FIXME: Change the way we handle the mileage submit with the mileage entry
    gas_check = tk.Checkbutton(ui.master, text="MPG Entry")
    gas_check.grid(row=4, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    total_label = tk.Label(ui.master, text="Total Paid:")
    total_label.grid(row=5, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    total_entry = ttk.Entry(ui.master, textvariable="", validate="key", validatecommand=(ui.float_vcmd, "%P"))
    total_entry.grid(row=5, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    gallons_label = tk.Label(ui.master, text="Gallons Bought:")
    gallons_label.grid(row=6, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    gallons_entry = ttk.Entry(ui.master, textvariable="", validate="key", validatecommand=(ui.float_vcmd, "%P"))
    gallons_entry.grid(row=6, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    #* Submit Area
    mile_submit = ttk.Button(ui.master, text="Enter Mileage", command=add_mileage)
    mile_submit.grid(row=7, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    back_button = ttk.Button(ui.master, text="Go Back", command=ui._show_main_screen)
    back_button.grid(row=8, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)

#* Mileage Helper
def add_mileage(ui):
    ui.db.add_mileage(ui.cars[ui.car_combo.current()]["CarID"],
                        ui.mileage_var.get(),
                        ui.date_var.get())
    
    messagebox.showinfo("Mileage Entered", "Your Mileage has been entered")
    
    ui._show_main_screen()