import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt


#* Mileage

def show_mileage_screen(ui):
    #TODO: Add a MPG Area, This make the _create_shared unuseable
    #TODO: Add number only for the mileage area
    #* Initialize Frame & Call DB
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)

    ui.car_var = tk.StringVar()
    ui.mileage_var = tk.IntVar()
    ui.date_var = tk.StringVar()


    title_label = tk.Label(ui.master, text="Enter Mileage", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=25)


    ui.cars = ui.db.get_all_cars()

    car_label = ttk.Label(ui.master, text="Car: ")
    car_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    ui.car_combo = ttk.Combobox(ui.master, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][0])
    ui.car_combo.grid(row=1, column=1, sticky="w", padx=10, pady=10)

    mileage_label = ttk.Label(ui.master, text="Mileage:")
    mileage_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)

    mileage_entry = ttk.Entry(ui.master, textvariable=ui.mileage_var, validate="key", validatecommand=(ui.vcmd, "%P"))
    mileage_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)

    mileage_date_label = ttk.Label(ui.master, text="Date of reading:")
    mileage_date_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    mileage_date = ttk.Entry(ui.master, textvariable=ui.date_var)
    ui.date_var.set(value=dt.date.today())
    mileage_date.grid(row=3, column=1, sticky="w", padx=10, pady=10)


    mile_submit = ttk.Button(ui.master, text="Enter Mileage", command=add_mileage)
    mile_submit.grid(row=4, columnspan=2, padx=10, pady=10)

    back_button = ttk.Button(ui.master, text="Go Back", command=ui._show_main_screen)
    back_button.grid(row=5, columnspan=2, padx=10, pady=10)

#* Mileage Helper
def add_mileage(ui):
    ui.db.add_mileage(ui.cars[ui.car_combo.current()]["CarID"],
                        ui.mileage_var.get(),
                        ui.date_var.get())
    
    messagebox.showinfo("Mileage Entered", "Your Mileage has been entered")
    
    ui._show_main_screen()