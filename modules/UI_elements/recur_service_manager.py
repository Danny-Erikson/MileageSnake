import tkinter as tk
from tkinter import ttk, messagebox

from ui_padding import *

#NOTE: self.cars is called at launch in tkinker_UI

#* Builders

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
    ui.car_var.set(ui.car_combo["values"][ui.car_index])
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
    #*Table Clean Up
    for widget in ui.service_table.winfo_children():
        info = widget.grid_info()
        if int(info["row"]) > 0:   # keep header row
            widget.destroy()
    
    #* Grab Data
    ui.car_index = ui.car_combo.current()
    services = ui.db.get_recurring_services_by_carID(ui.cars[ui.car_index]["CarID"])
    
    day_sort(services, find_days_only(services))
    
    #* Build Table
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
        
        service_in_miles = tk.Label(ui.service_table, text=f"{service["DueMileage"]:,}" if service["DueMileage"] is not None else "")
        service_in_miles.grid(row=row_count, column=2, sticky="ew")
        
        service_in_days = tk.Label(ui.service_table, text=f"{day_formatter(service["IntervalValue"], service["IntervalUnit"])}" if service["IntervalValue"] is not None else "")
        service_in_days.grid(row=row_count, column=3, sticky="ew")
        
        remove_service_button = tk.Button(
            ui.service_table,
            text="Remove Service",
            command=lambda serviceID=service["ServiceId"]: remove_service(ui, serviceID=serviceID)
        )
        remove_service_button.grid(row=row_count, column=4, sticky="ew")
        
        row_count += 1
    
    #* Bottom of screen
    add_new = tk.Button(ui.service_table, text="Add New Service", command=lambda: show_service_form(ui))
    add_new.grid(row=row_count + 2, column=0, columnspan=5, padx=BUTTON_X, pady=BUTTON_Y)
    go_back = tk.Button(ui.service_table, text="Go Back", command=ui._show_main_screen)
    go_back.grid(row=row_count + 3, column=0, columnspan=5, padx=BUTTON_X, pady=BUTTON_Y)

def show_service_form(ui, serviceID=None, editing=False):
    #* Initialize frame and Tk variables
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    ui.master.columnconfigure(2, weight=1)
    
    ui.name_var = tk.StringVar()
    ui.due_mileage_var = tk.StringVar()
    ui.time_value_var = tk.StringVar()
    ui.time_unit_var = tk.StringVar()
    
    #* Conditional rendering
    # The editing flag is True if the user clicked the edit button to call the function
    # if so change the title of the frame and pass in DB data from the service ID
    # also change the function called when we click the submit button
    if editing:
        title_label = ttk.Label(ui.master, text="Edit Service", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=3, pady=TITLE_Y)
        
        # call db for values
        service = ui.db.get_recurring_services_by_ID(serviceID)
        
        ui.name_var.set(value=service["Name"])
        ui.due_mileage_var.set(value=service["DueMileage"] or "")
        ui.time_value_var.set(value=service["IntervalValue"] or "")
        ui.time_unit_var.set(value=service["IntervalUnit"] or "")
        
        submit_button = ttk.Button(ui.master, text="Submit", command=lambda serviceID=service["ServiceId"]:edit_service(ui, serviceID))
        submit_button.grid(row= 5, columnspan=3, padx=BUTTON_X, pady=BUTTON_Y)
    
    else:
        title_label = ttk.Label(ui.master, text="Add a New Service", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=3, pady=TITLE_Y)
        
        submit_button = ttk.Button(ui.master, text="Submit", command=lambda: add_service(ui))
        submit_button.grid(row= 5, columnspan=3, padx=BUTTON_X, pady=BUTTON_Y)
    
    #* Building of Shared Elements
    car_label = ttk.Label(ui.master, text=f"Service for: {ui.cars[ui.car_index]["Year"]} {ui.cars[ui.car_index]["Make"]} {ui.cars[ui.car_index]["Model"]}", font=(14))
    car_label.grid(row=1, columnspan=5, padx=10, pady=10)
    
    name_label = ttk.Label(ui.master, text="Name:")
    name_label.grid(row=2, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    name_entry = ttk.Entry(ui.master, textvariable=ui.name_var)
    name_entry.grid(row=2, column=1, sticky="we", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_label = ttk.Label(ui.master, text="Due Mileage:")
    mileage_label.grid(row=3, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    mileage_entry = ttk.Entry(ui.master, textvariable=ui.due_mileage_var, validate="key", validatecommand=(ui.int_vcmd, "%P"))
    mileage_entry.grid(row=3, column=1, sticky="we", padx=ENTRY_X, pady=ENTRY_Y)
    
    time_label = ttk.Label(ui.master, text="Due Every:")
    time_label.grid(row=4, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    time_entry = ttk.Entry(ui.master, textvariable=ui.time_value_var, validate="key", validatecommand=(ui.int_vcmd, "%P"))
    time_entry.grid(row=4, column=1, sticky="we", padx=ENTRY_X, pady=ENTRY_Y)
    time_combo = ttk.Combobox(ui.master, textvariable=ui.time_unit_var, state="readonly")
    time_combo["values"] = ["days", "months", "years"]
    time_combo.grid(row=4, column=2, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    back_button = ttk.Button(ui.master, text="Go Back", command=lambda: show_recur_service_manager(ui))
    back_button.grid(row= 6, columnspan=3, padx=BUTTON_X, pady=BUTTON_Y)

#* Helpers

def validate_inputs(ui):
    if ui.name_var.get() == "":
        messagebox.showerror("Input Error", "Name can not be blank")
        return False
    
    if ui.due_mileage_var.get() == "" and ui.time_value_var.get() == "":
        messagebox.showerror("Input Error", "Mileage Due and Due every cannot both be blank\nOne or both must be filled")
        return False
    
    if ui.time_value_var.get() != "" and ui.time_unit_var.get() == "":
        messagebox.showerror("Input Error", "Select a timeframe from the box")
        return False
    
    return True

def add_service(ui):
    if not validate_inputs(ui):
        return
    
    safe_inputs = (ui.name_var.get(),
                    ui.cars[ui.car_index]["CarID"],
                    ui.due_mileage_var.get() or None)
    
    if ui.time_value_var.get() == "":
        sanitized_inputs = (*safe_inputs, None, None)
    else:
        sanitized_inputs = (*safe_inputs, ui.time_value_var.get(), ui.time_unit_var.get())
    
    ui.db.add_recurring_services(*sanitized_inputs)
    
    show_recur_service_manager(ui)

def edit_service(ui, serviceID):
    if not validate_inputs(ui):
        return
    
    safe_inputs = (ui.name_var.get(),
                    ui.due_mileage_var.get() or None)
    
    if ui.time_value_var.get() == "":
        sanitized_inputs = (*safe_inputs, None, None)
    else:
        sanitized_inputs = (*safe_inputs, ui.time_value_var.get(), ui.time_unit_var.get())
    
    ui.db.update_recurring_service(*sanitized_inputs, serviceID)
    
    show_recur_service_manager(ui)

def remove_service(ui, serviceID):
    service = ui.db.get_recurring_services_by_ID(serviceID)
    confirmed = messagebox.askyesno("Delete Service", f"Are you sure you want to delete {service["Name"]}")
    if confirmed:
        ui.db.remove_recurring_service(serviceID)
        on_car_change(ui)

def find_days_only(service):
    days = [s for s in service if s["DueMileage"] is None]
    service[:] = [s for s in service if s["DueMileage"] is not None]
    return days

def day_sort(service, split):
    # Take this a future todo but at some point it pipe in the cars AVG Miles per day to this
    # It would be closer to the intend of this sort which is to sort the services based on frequency
    # we could probably do this with a cached MPD and convert DueDays to miles and compare that way 
    while split != []:
        i = 0
        found = False
        match split[0]["IntervalUnit"]:
            case "days":
                i_days = split[0]["IntervalValue"]
            case "months":
                i_days = int(split[0]["IntervalValue"]) * 30
            case "years":
                i_days = int(split[0]["IntervalValue"]) * 365
        
        while not found:
            next_service = service[i+1]
            
            match next_service["IntervalUnit"]:
                case None:
                    c_days = 0
                case "days":
                    c_days = next_service["IntervalValue"]
                case "months":
                    c_days = int(next_service["IntervalValue"]) * 30
                case "years":
                    c_days = int(next_service["IntervalValue"]) * 365
            
            if i_days >= c_days:
                i += 1
            else:
                service.insert(i, split[0])
                split.pop(0)
                found = True

def day_formatter(value, unit):
    if value == 1:
        return f"{value} {unit[:-1]}"
    else:
        return f"{value} {unit}"
