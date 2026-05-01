import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt

from ui_padding import *


def show_service_screen(ui):
    #*Check for cars to avoid error
    if ui.cars == []:
        ui.no_id_reroute()
        return
    
    #* Initialize Frame
    ui._clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    
    ui.service_mode_var = tk.StringVar(value="reoccurring")
    
    ui.car_var = tk.StringVar()
    ui.mileage_var = tk.StringVar()
    ui.date_var = tk.StringVar()
    ui.name_var = tk.StringVar()
    
    title_label = tk.Label(ui.master, text="Enter Service", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)
    
    car_label = ttk.Label(ui.master, text="Car: ")
    car_label.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.car_combo = ttk.Combobox(ui.master, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][ui.car_index])
    ui.car_combo.bind("<<ComboboxSelected>>", lambda e: build_service_editor(ui))
    ui.car_combo.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_label = ttk.Label(ui.master, text="Mileage:")
    mileage_label.grid(row=2, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_entry = ttk.Entry(ui.master, textvariable=ui.mileage_var, validate="key", validatecommand=(ui.int_vcmd, "%P"))
    mileage_entry.grid(row=2, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_date_label = ttk.Label(ui.master, text="Date of service:")
    mileage_date_label.grid(row=3, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    mileage_date = ttk.Entry(ui.master, textvariable=ui.date_var)
    ui.date_var.set(value=dt.date.today())
    mileage_date.grid(row=3, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    reoccurring_radio = ttk.Radiobutton(ui.master,text="Reoccurring Service",variable=ui.service_mode_var,value="reoccurring",command=lambda: build_service_editor(ui))
    reoccurring_radio.grid(row=4, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    general_radio = ttk.Radiobutton(ui.master, text="General Service", variable=ui.service_mode_var, value="general", command=lambda: build_service_editor(ui))
    general_radio.grid(row=4, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.service_editor = tk.Frame(ui.master)
    ui.service_editor.grid(row=5, column=0, columnspan=2, sticky="ew")
    ui.service_editor.columnconfigure(0, weight=1)
    ui.service_editor.columnconfigure(1, weight=1)
    ui.service_editor.columnconfigure(2, weight=1)
    ui.service_editor.columnconfigure(3, weight=1)

    build_service_editor(ui)

    back_button = ttk.Button(ui.master, text="Go Back", command=ui._show_main_screen)
    back_button.grid(row=9, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)

def build_service_editor(ui):
    for widget in ui.service_editor.winfo_children():
        widget.destroy()
    
    mode = ui.service_mode_var.get()
    if mode == "general":
        build_general_service(ui)
    elif mode == "reoccurring":
        build_reoccurring_service(ui)

def build_general_service(ui):
    name_label = ttk.Label(ui.service_editor, text="Name:")
    name_label.grid(row=0, column=1, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    name_entry = ttk.Entry(ui.service_editor, textvariable=ui.name_var)
    name_entry.grid(row=0, column=2, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)
    
    description_label = tk.Label(ui.service_editor, text="Note:")
    description_label.grid(row=1, column=1, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    
    ui.description_box = tk.Text(ui.service_editor, width=40, height=10)
    ui.description_box.grid(row=1, column=2, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)

    submit_button = ttk.Button(ui.service_editor, text="Submit", command= lambda: add_one_service(ui))
    submit_button.grid(row=2, column=1, columnspan=2, padx=ENTRY_X, pady=ENTRY_Y)

def build_reoccurring_service(ui):
    ui.car_index = ui.car_combo.current()
    services = ui.db.get_recurring_services_by_carID(ui.cars[ui.car_index]["CarId"])
    
    ui.selected = {}
    ui.notes = {}
    ui.note_entries = {}
    row_count = 0
    
    def toggle_note(service_id):
        if ui.selected[service_id].get():
            ui.note_entries[service_id].config(state="normal")
        else:
            ui.note_entries[service_id].config(state="disabled")
    
    for s in services:
        service_id = s["ServiceId"]
        
        ui.selected[service_id] = tk.BooleanVar()
        ui.notes[service_id] = tk.StringVar()
        ui.notes[service_id].set(f"{s["AutoNote"] or ""}")
        
        tk.Checkbutton(ui.service_editor, text=s["Name"], variable=ui.selected[service_id], command=lambda sid=service_id: toggle_note(sid)).grid(row=row_count, column=1, sticky="w")
        tk.Label(ui.service_editor, text="Notes: ").grid(row=row_count, column=1, sticky="e")
        ui.note_entries[service_id] = tk.Entry(ui.service_editor, textvariable=ui.notes[service_id], state="disabled")
        ui.note_entries[service_id].grid(row=row_count, column=2, ipadx=75, sticky="w")
        
        row_count += 1

    tk.Button(ui.service_editor, text="Submit", command=lambda: add_reoccurring_services(ui)).grid(row=row_count + 1, columnspan=4)

def validate_inputs(ui):
    if ui.mileage_var.get() == "":
        messagebox.showerror("Input Error", "Mileage can not be blank")
        return False
    
    last_reading = ui.db.get_mileage_by_ID(ui.cars[ui.car_combo.current()]["CarId"])
    if last_reading is not None:
        if int(ui.mileage_var.get()) < last_reading["OdometerReading"] :
            messagebox.showerror("Input Error", "Mileage must be bigger than less reading")
            return False
    
    if not ui.is_valid_date(ui.date_var.get()):
        messagebox.showerror("Input Error", "Invalid date format.\nUse YYYY-MM-DD (e.g. 2026-07-25).")
        return False
    
    if dt.datetime.strptime(ui.date_var.get(), "%Y-%m-%d").date() > dt.date.today():
        messagebox.showerror("Input Error", "Date can not be in the future")
        return False
    
    return True

def add_one_service(ui):
    if not validate_inputs(ui):
        return
    
    confirmed = messagebox.askyesno("Confirm Service Details", f'Enter {ui.name_var.get()} at {ui.mileage_var.get()} miles\nwith a description of "{ui.description_box.get("1.0", "end")}"')
    if not confirmed:
        return
    
    mileage_check = ui.db.mileage_match(ui.cars[ui.car_index]["CarId"], ui.mileage_var.get(), ui.date_var.get())
    if mileage_check != None:
        mileage_id = mileage_check["MileageId"]
    else:
        mileage_id = ui.db.add_mileage(ui.cars[ui.car_index]["CarId"], ui.mileage_var.get(), ui.date_var.get())
    
    ui.db.add_service(ui.name_var.get(), ui.cars[ui.car_index]["CarId"], None, mileage_id, ui.description_box.get("1.0", "end"))
    
    messagebox.showinfo("Service Entered", "Service has been entered")
    ui._show_main_screen()

def add_reoccurring_services(ui):
    if not validate_inputs(ui):
        return
    
    selected_ids = [sid for sid, var in ui.selected.items() if var.get()]
    if selected_ids == []:
        messagebox.showerror("Input Error", "Please select services to enter")
        return
    
    message = f"Enter Services at {ui.mileage_var.get()}\n"
    for ser_id in selected_ids:
        s = ui.db.get_recurring_services_by_ID(ser_id)
        message += f"{s["Name"]}\n"
    
    confirmed = messagebox.askyesno("Confirm Service Details", f"{message[:-1]}")
    if not confirmed:
        return
    
    car_id = ui.cars[ui.car_index]["CarId"]
    
    mileage_check = ui.db.mileage_match(car_id, ui.mileage_var.get(), ui.date_var.get())
    if mileage_check != None:
        mileage_id = mileage_check["MileageId"]
    else:
        mileage_id = ui.db.add_mileage(car_id, ui.mileage_var.get(), ui.date_var.get())
    
    for ser_id in selected_ids:
        ser = ui.db.get_recurring_services_by_ID(ser_id)
        if ui.notes[ser_id].get() != "":
            if ui.notes[ser_id].get() != ser["AutoNote"]:
                update = messagebox.askquestion("Update AutoNote", f'We noticed you updated the note for "{ser["Name"]}"\nDid you want to update it from\n"{ser["AutoNote"]}"\nto\n"{ui.notes[ser_id].get()}"')
                if update:
                    ui.db.update_auto_note_by_id(ui.notes[ser_id].get(), ser_id)
                    ui.db.add_service(ser["Name"], car_id, ser_id, mileage_id, ui.notes[ser_id].get())
                else:
                    ui.db.add_service(ser["Name"], car_id, ser_id, mileage_id, ser["AutoNote"])
            else:
                ui.db.add_service(ser["Name"], car_id, ser_id, mileage_id, ser["AutoNote"])
        else:
            ui.db.add_service(ser["Name"], car_id, ser_id, mileage_id, None)
    
    messagebox.showinfo("Service Entered", "Service has been entered")
    ui._show_main_screen()

