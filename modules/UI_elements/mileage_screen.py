import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt

from ui_padding import *

#NOTE: self.cars is called at launch in tkinker_UI

#* Mileage

def show_mileage_screen(ui):
    #* Initialize Frame
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    
    ui.car_var = tk.StringVar()
    ui.mileage_var = tk.StringVar()
    ui.date_var = tk.StringVar()
    ui.mpg_var = tk.BooleanVar()
    ui.total_paid_var = tk.StringVar()
    ui.gallons_bought_var = tk.StringVar()
    ui.full_up_var = tk.BooleanVar(value=True)
    
    title_label = tk.Label(ui.master, text="Enter Mileage", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
    
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
    
    #* Fuel Area
    mpg_check = tk.Checkbutton(ui.master,text="MPG Entry",variable=ui.mpg_var, command=lambda: mpg_toggle(ui))
    mpg_check.grid(row=4, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    ui.total_label = tk.Label(ui.master, text="Total Paid:")
    ui.total_label.grid(row=5, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.total_entry = ttk.Entry(ui.master, textvariable=ui.total_paid_var, validate="key", validatecommand=(ui.float_vcmd, "%P"), state="disabled")
    ui.total_entry.grid(row=5, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.gallons_label = tk.Label(ui.master, text="Gallons Bought:")
    ui.gallons_label.grid(row=6, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.gallons_entry = ttk.Entry(ui.master, textvariable=ui.gallons_bought_var, validate="key", validatecommand=(ui.float_vcmd, "%P"), state="disabled")
    ui.gallons_entry.grid(row=6, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.full_up_check = tk.Checkbutton(ui.master, text="Filled to Full", variable=ui.full_up_var, state="disabled")
    ui.full_up_check.grid(row=7, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    #* Submit Area
    mile_submit = ttk.Button(ui.master, text="Enter Mileage", command=lambda: add_mileage(ui))
    mile_submit.grid(row=8, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    back_button = ttk.Button(ui.master, text="Go Back", command=ui._show_main_screen)
    back_button.grid(row=9, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)

#* Mileage Helper
def add_mileage(ui):
    if not validate_inputs(ui):
        return
    
    mileageID = ui.db.add_mileage(ui.cars[ui.car_combo.current()]["CarID"],
                        ui.mileage_var.get(),
                        ui.date_var.get())
    message = "Your mileage has been entered"

    if ui.mpg_var.get() == True:
        ui.db.add_fuel(mileageID,
                    ui.gallons_bought_var.get(),
                    ui.total_paid_var.get(),
                    1 if ui.full_up_var.get() else 0)
                    # Thank you SQLite for making me use this absolutely ""beautiful"" line 
                    # Instead of just having a Boolean Type
        message = "Your mileage and fuel has been entered"
    
    messagebox.showinfo("Mileage Entered", f"{message}")
    
    ui._show_main_screen()

def mpg_toggle(ui):
    if ui.mpg_var.get():
        ui.total_entry.config(state="normal")
        ui.gallons_entry.config(state="normal")
        ui.full_up_check.config(state="normal")
    else:
        ui.total_entry.config(state="disabled")
        ui.gallons_entry.config(state="disabled")
        ui.full_up_check.config(state="disabled")

def validate_inputs(ui):
    if ui.mileage_var.get() == "":
        messagebox.showerror("Input Error", "Mileage can not be blank")
        return False
    
    last_reading = ui.db.get_mileage_by_ID(ui.cars[ui.car_combo.current()]["CarID"])
    if last_reading is not None:
        if int(ui.mileage_var.get()) < last_reading["OdometerReading"] :
            messagebox.showerror("Input Error", "Mileage must be bigger than less reading")
            return False
    
    if not ui.is_valid_date(ui.date_var.get()):
        messagebox.showerror("Input Error", "Invalid date format.\nUse YYYY-MM-DD (e.g. 2026-04-01).")
        return False
    
    if dt.datetime.strptime(ui.date_var.get(), "%Y-%m-%d").date() > dt.date.today():
        messagebox.showerror("Input Error", "Date can not be in the future")
        return False
    
    if ui.mpg_var.get():
        if ui.total_paid_var.get() == "":
            messagebox.showerror("Input Error", "Total paid can not be blank")
            return False
        
        if ui.gallons_bought_var.get() == "":
            messagebox.showerror("Input Error", "Gallons bought can not be blank")
            return False
    
    return True
