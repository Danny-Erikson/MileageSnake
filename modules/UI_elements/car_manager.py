import tkinter as tk
from tkinter import ttk, messagebox

from ui_padding import *

#* Car Manager

#NOTE: self.cars is called at launch in tkinker_UI and we update it as needed. This is to reduce db calls

def show_car_manager(ui):
    #* Initialize Frame
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    ui.master.columnconfigure(2, weight=1)
    ui.master.columnconfigure(3, weight=1)
    ui.master.columnconfigure(4, weight=1)
    
    #* Build top of table
    title_label = tk.Label(ui.master, text="Cars", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=5, pady=TITLE_Y)
    
    car_label = tk.Label(ui.master, text="Car")
    car_label.grid(row=1, column=1, sticky="ew")
    license_label = tk.Label(ui.master, text="License plate")
    license_label.grid(row=1, column=2, sticky="ew")
    vin_label = tk.Label(ui.master, text="VIN Number")
    vin_label.grid(row=1, column=3, sticky="ew")
    
    #* Build rows for car table 
    # This for loop is to build a table based on the number of entry in the cars table
    # The .bind on each element to allow the text to be copyable 
    row_count = 2
    for car in ui.cars:
        edit_button = tk.Button(ui.master, text="🖉", command=lambda carID=car["CarID"]: show_car_form(ui, editing=True, carID=carID))
        edit_button.grid(row=row_count, column=0, sticky="ew")
        car_name = tk.Label(ui.master, text=f"{car["Year"]} {car["Make"]} {car["Model"]} {car["Trim"] or ""}")
        car_name.bind("<Button-1>", copy_text)
        car_name.grid(row=row_count, column=1, sticky="ew")
        car_vin = tk.Label(ui.master, text=car["LicensePlate"])
        car_vin.bind("<Button-1>", copy_text)
        car_vin.grid(row=row_count, column=2, sticky="ew")
        car_license = tk.Label(ui.master, text=car["VINNumber"])
        car_license.bind("<Button-1>", copy_text)
        car_license.grid(row=row_count, column=3, sticky="ew")
        remove_car_button = tk.Button(ui.master, text="Remove Car", command=lambda carID=car["CarID"]: remove_car(ui, carID=carID))
        remove_car_button.grid(row=row_count, column=4, sticky="ew")
        row_count += 1
    
    #* Below the table elements
    copy_inst = tk.Label(ui.master, text="Click on car values to copy to clipboard")
    copy_inst.grid(row=row_count + 1, column=0, columnspan=5, padx=BUTTON_X, pady=BUTTON_Y)
    add_new = tk.Button(ui.master, text="Add New Car", command=lambda: show_car_form(ui))
    add_new.grid(row=row_count + 2, column=0, columnspan=5, padx=BUTTON_X, pady=BUTTON_Y)
    go_back = tk.Button(ui.master, text="Go Back", command=ui.show_advanced_area)
    go_back.grid(row=row_count + 3, column=0, columnspan=5, padx=BUTTON_X, pady=BUTTON_Y)

def show_car_form(ui, editing=False, carID=None):
    #* Initialize frame and Tk variables
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    
    ui.year_var = tk.StringVar()
    ui.make_var = tk.StringVar()
    ui.model_var = tk.StringVar()
    ui.trim_var = tk.StringVar()
    ui.license_var = tk.StringVar()
    ui.vin_var = tk.StringVar()
    
    #* Conditional rendering
    # The editing flag is True if the user clicked the edit button to call the function
    # if so change the title of the frame and pass in DB data from the car's ID
    # also change the function called when we click the submit button
    if editing:
        title_label = ttk.Label(ui.master, text="Edit Car Information", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
        
        # call db for values
        car = ui.db.get_car_by_ID(carID)
        
        ui.year_var.set(value=car["Year"])
        ui.make_var.set(value=car["Make"])
        ui.model_var.set(value=car["Model"])
        ui.trim_var.set(value=car["Trim"] or "")
        ui.license_var.set(value=car["LicensePlate"] or "")
        ui.vin_var.set(value=car["VINNumber"] or "")
        
        submit_button = ttk.Button(ui.master, text="Submit", command=lambda carID=car["CarID"]:edit_car(ui, carID))
        submit_button.grid(row= 7, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    else:
        title_label = ttk.Label(ui.master, text="Add a New Car", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
        
        submit_button = ttk.Button(ui.master, text="Submit", command=lambda: add_new_car(ui))
        submit_button.grid(row= 7, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)
    
    #* Building of Shared Elements 
    year_label = ttk.Label(ui.master, text="Year:")
    year_label.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    year_entry = ttk.Entry(ui.master, textvariable=ui.year_var, validate="key", validatecommand=(ui.int_vcmd, "%P"))
    year_entry.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    make_label = ttk.Label(ui.master, text="Make:")
    make_label.grid(row=2, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    make_entry = ttk.Entry(ui.master, textvariable=ui.make_var)
    make_entry.grid(row=2, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    model_label = ttk.Label(ui.master, text="Model:")
    model_label.grid(row=3, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    model_entry = ttk.Entry(ui.master, textvariable=ui.model_var)
    model_entry.grid(row=3, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    trim_label = ttk.Label(ui.master, text="Trim:")
    trim_label.grid(row=4, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    trim_entry = ttk.Entry(ui.master, textvariable=ui.trim_var)
    trim_entry.grid(row=4, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    license_label = ttk.Label(ui.master, text="License Plate:")
    license_label.grid(row=5, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    license_entry = ttk.Entry(ui.master, textvariable=ui.license_var)
    license_entry.grid(row=5, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    vin_label = ttk.Label(ui.master, text="VIN Number:")
    vin_label.grid(row=6, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    vin_entry = ttk.Entry(ui.master, textvariable=ui.vin_var)
    vin_entry.grid(row=6, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    back_button = ttk.Button(ui.master, text="Go Back", command=lambda: show_car_manager(ui))
    back_button.grid(row= 8, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)

#* Car Manager Helper

def validate_inputs(ui):
    if ui.year_var.get() == "":
        messagebox.showerror("Input Error", "Year can not be blank")
        return False
    
    if ui.make_var.get() == "":
        messagebox.showerror("Input Error", "Make can not be blank")
        return False
    
    if ui.model_var.get() == "":
        messagebox.showerror("Input Error", "Model can not be blank")
        return False
    
    if len(ui.vin_var.get()) == 17:
        messagebox.showerror("Input Error", "VIN must be 17 characters long")
        return False
    
    return True

def add_new_car(ui):
    if not validate_inputs(ui):
        return
    
    car_id = ui.db.add_car(ui.vin_var.get().upper() or None,
                    ui.license_var.get().upper() or None,
                    int(ui.year_var.get()),
                    ui.make_var.get(),
                    ui.model_var.get(),
                    ui.trim_var.get() or None,
                    )
    
    #* Ask about optional services
    print(car_id)
    op_list = ui.db.get_asking_temp_services()
    for service in op_list:
        user_response = messagebox.askyesno("Add Service", f"{service["Question"]}?")
        if user_response:
            ui.db.add_recurring_services(service["Name"], car_id, service["DueMileage"], service["IntervalValue"], service["IntervalUnit"])
    
    ui.cars = ui.db.get_all_cars()
    show_car_manager(ui)

def edit_car(ui, carID):
    if not validate_inputs(ui):
        return
    
    ui.db.update_car(ui.vin_var.get().upper() or None,
                    ui.license_var.get().upper() or None,
                    int(ui.year_var.get()),
                    ui.make_var.get(),
                    ui.model_var.get(),
                    ui.trim_var.get() or None,
                    carID
                    )
    
    ui.cars = ui.db.get_all_cars()
    show_car_manager(ui)

def remove_car(ui, carID):
    car = ui.db.get_car_by_ID(carID)
    
    confirmed = messagebox.askyesno("Delete Car", f"Are you sure you want to delete {car["Year"]} {car["Make"]} {car["Model"]}")
    if confirmed:
        mile_count = ui.db.get_mileage_by_ID(carID)
        if mile_count and len(mile_count) > 3:
            messagebox.showinfo("Double Check", "Please go to the terminal to confirm the removal")
            double = input(f'CAUTION: You are about to delete a car with {len(mile_count)} entries, type "Yes" if you meant to do this: \n')
            if double == "Yes":
                safe_to_delete = True
            else:
                print("Operation aborted, if you believe this is a mistake, make sure you type Y-e-s")
        else:
            safe_to_delete = True
        
        if safe_to_delete:
            ui.db.remove_car(carID)
            ui.cars = ui.db.get_all_cars()
            show_car_manager(ui)

def copy_text(event):
    widget = event.widget
    root = widget.winfo_toplevel()
    
    text = widget.cget("text")
    if text != '':
        widget.clipboard_clear()
        widget.clipboard_append(text)
        
        x = event.x_root - root.winfo_rootx() + 10
        y = event.y_root - root.winfo_rooty() + 10
        
        msg = ttk.Label(root, text="Copied!")
        msg.place(x=x, y=y)
        root.after(800, msg.destroy)
