import tkinter as tk
from tkinter import ttk, messagebox

import xlsxwriter

from datetime import datetime, date

from modules.Number_crunchers.calculate_mileage_pairs import calculate_mileage_pairs
from modules.Number_crunchers.mileage_per_day import calculate_mileage_per_day
from modules.Number_crunchers.prep_services_for_export import prep_services_for_export

from ui_padding import *

#NOTE: self.cars is called at launch in tkinker_UI and we update it as needed. This is to reduce db calls

#* Builders
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
    
    submit_button = ttk.Button(ui.option_table, text="Generate Report", command=lambda:excel_export(ui))
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

#* Calculation
def calculate_re_service_data(ui, car_id):
    #* Get avg miles per day 
    mileage = ui.db.get_recent_mileage_by_car(car_id)
    latest_mileage = mileage[-1]
    mileage_pairs = calculate_mileage_pairs(mileage)
    mileage_avgs = calculate_mileage_per_day(mileage_pairs)
    avg_miles_per_day = round(sum(mileage_avgs) / len(mileage_avgs), 3)
    
    #* get re_service Data
    services = []
    for s in ui.db.get_recurring_services_by_carID(car_id):
        recent = ui.db.find_last_service_done(s["ServiceId"])
        if recent != None:
            services.append(recent)
    
    data = [latest_mileage]
    for ser in services:
        prepped = prep_services_for_export(ser, latest_mileage, avg_miles_per_day)
        data.append(prepped)
    
    return data

def excel_export(ui):
    if ui.car_var.get() == "ALL":
        cars = ui.cars
    else:
        selected_car_text = ui.car_var.get()
        
        cars = [
            car for car in ui.cars
            if f"{car['Year']} {car['Make']} {car['Model']}" == selected_car_text
        ]
    
    today = date.today()
    with xlsxwriter.Workbook(f'Reports/Services Due Report {today.strftime("%m-%d-%Y")}.xlsx') as workbook:
        base_format = {
            "align": "center",
            "valign": "vcenter",
            "font_size": 16,
        }
        
        string_format = workbook.add_format(base_format)
        
        num_format = workbook.add_format({
            **base_format,
            "num_format": "#,##0",
        })
        
        for car in cars:
            row_num = 0 
            #* Grab Data for Outside
            data = calculate_re_service_data(ui, car["CarId"])
            
            title_format = workbook.add_format({
                **base_format,
                "border": 1,
                "bg_color": car["Color"],
                "font_color": ui.text_color_for_bg(car["Color"]),
            })
            
            #* Crate workbook
            worksheet = workbook.add_worksheet(car["Model"])
            worksheet.set_column('A:F',30)
            
            #* Top of Table
            worksheet.set_row(row_num, 30)
            worksheet.merge_range('A1:F1',f'{car["Year"]} {car["Make"]} {car["Model"]} {car["Trim"] or ""}', title_format)
            row_num += 1
            
            worksheet.set_row(row_num, 30)
            worksheet.write("A2", "Latest Mileage:", string_format)
            worksheet.write("B2", data[0]["OdometerReading"], num_format)
            data.pop(0)
            worksheet.write("E2", "Date of next service:", string_format)
            row_num += 1
            
            worksheet.set_row(row_num, 30)
            worksheet.write("A3", "Service", string_format)
            worksheet.write("B3", "Mileage Done At", string_format)
            worksheet.write("C3", "Due Every", string_format)
            worksheet.write("D3", "Mileage Due", string_format)
            worksheet.write("E3", "Date Due", string_format)
            worksheet.write("F3", "Est Date of Service", string_format)
            row_num += 1
            
            next_ser_date = "12/31/8008"
            for s in data:
                worksheet.set_row(row_num, 30)
                worksheet.write(row_num, 0, s["Name"], string_format)
                worksheet.write(row_num, 1, s["MileageDoneAt"], num_format)
                worksheet.write(row_num, 2, s["DueEveryMileage"], num_format)
                worksheet.write(row_num, 3, s["NextServiceMiles"], num_format)
                worksheet.write(row_num, 4, s["DueDate"], string_format)
                worksheet.write(row_num, 5, s["EstDate"], string_format)
                row_num += 1
                
                date1 = datetime.strptime(next_ser_date, "%m/%d/%Y").date()
                date2 = datetime.strptime(s["EstDate"], "%m/%d/%Y").date()
                
                next_ser_date = date1 if abs(date1 - today) < abs(date2 - today) else date2
            
            row_num += 1
            worksheet.set_row(row_num, 30)
            worksheet.merge_range(row_num, 0, row_num, 6,f'Date of Report: {today.strftime("%m/%d/%Y")}', string_format)
            
            worksheet.write('F2', next_ser_date.strftime("%m/%d/%Y") if next_ser_date != "12/31/8008" else "", string_format)
    messagebox.showinfo("Report Ready", "Report has Been saved")
    ui.show_reports_screen()

def HTML_export(ui, car_ids):
    pass
    # Take a list of carids  and call calculate re data
    # Take list of [{car 1}}{car 2}{car 3}] and each to HTML
