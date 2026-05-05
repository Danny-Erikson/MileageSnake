import tkinter as tk
from tkinter import ttk, messagebox

from ui_padding import *

#NOTE: self.cars is called at launch in tkinker_UI and we update it as needed. This is to reduce db calls

def show_due_service_config(ui):
    #* Initialize Frame
    ui.clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    
    ui.car_var = tk.StringVar()
    ui.type_var = tk.StringVar(value="Excel")
    ui.display_var = tk.StringVar()
    
    #* Top of the screen 
    title_label = tk.Label(ui.master, text="Services Done Report", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
    
    #* Middle of the screen
    excel_radio = ttk.Radiobutton(ui.master,text="Excel",variable=ui.type_var,value="Excel",command=lambda: on_type_change(ui))
    excel_radio.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    html_radio = ttk.Radiobutton(ui.master, text="HTML", variable=ui.type_var, value="HTML", command=lambda: on_type_change(ui))
    html_radio.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.option_table = tk.Frame(ui.master)
    ui.option_table.grid(row=2, column=0, columnspan=2, sticky="ew")
    ui.option_table.columnconfigure(0, weight=1)
    ui.option_table.columnconfigure(1, weight=1)
    
    on_type_change(ui)
    
    #* Bottom of screen
    back_button = ttk.Button(ui.master, text="Go Back", command=ui.show_reports_screen)
    back_button.grid(row=3, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)

def on_type_change(ui):
    #*Table Clean Up
    for widget in ui.option_table.winfo_children():
        widget.destroy()
    
    if ui.type_var.get() == "Excel":
        build_excel_options(ui)
    else:
        build_html_options(ui)

def build_excel_options(ui):
    car_label = ttk.Label(ui.option_table, text="Car:")
    car_label.grid(row=0, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.car_combo = ttk.Combobox(ui.option_table, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = ["ALL"] + [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][ui.car_index])
    ui.car_combo.grid(row=0, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    submit_button = ttk.Button(ui.option_table, text="Generate Report", command="")
    submit_button.grid(row=1, columnspan=2, padx=ENTRY_X, pady=ENTRY_Y)

def build_html_options(ui):
    car_label = ttk.Label(ui.option_table, text="Car:")
    car_label.grid(row=0, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.car_combo = ttk.Combobox(ui.option_table, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = ["ALL"] + [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][ui.car_index])
    ui.car_combo.grid(row=0, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    display_type_label = ttk.Label(ui.option_table, text="Display Type:")
    display_type_label.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    display_type_combo = ttk.Combobox(ui.option_table, textvariable=ui.display_var, state="readonly")
    display_type_combo["values"] = ["Card", "Table"]
    ui.display_var.set(display_type_combo["values"][0])
    display_type_combo.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    submit_button = ttk.Button(ui.option_table, text="Generate Report", command="")
    submit_button.grid(row=2, columnspan=2, padx=ENTRY_X, pady=ENTRY_Y)
