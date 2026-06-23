import tkinter as tk
from tkinter import ttk, messagebox

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from collections import defaultdict

from modules.Number_crunchers.calculate_mileage_pairs import calculate_mileage_pairs

import xlsxwriter

from ui_padding import *


def show_mileage_report_config(ui):
    ui.clear_frame()

    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)

    ui.car_var = tk.StringVar()
    ui.report_list = []

    # Last 6 months by default
    ui.start_date = tk.StringVar(
        value=(date.today() - relativedelta(months=6)))
    ui.end_date = tk.StringVar(value=date.today())

    ui.cars_with_gas = ui.db.mileage_screen_cars()

    if not ui.cars_with_gas:
        ui.no_fuel_reroute()
        return

    title_label = tk.Label(
        ui.master,
        text="Mileage Report",
        font=("Arial", 16)
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)

    ui.option_table = tk.Frame(ui.master)
    ui.option_table.grid(row=1, column=0, columnspan=2, sticky="ew")

    ui.option_table.columnconfigure(0, weight=1)
    ui.option_table.columnconfigure(1, weight=1)

    build_excel_options(ui)

    back_button = ttk.Button(
        ui.master,
        text="Go Back",
        command=ui.show_reports_screen
    )
    back_button.grid(row=2, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)


def car_display_name(car):
    return f"{car['Year']} {car['Make']} {car['Model']}"


def update_car_combo_values(ui):
    available_cars = [
        car_display_name(car)
        for car in ui.cars_with_gas
        if car_display_name(car) not in ui.report_list
    ]

    ui.car_combo["values"] = available_cars

    if available_cars:
        ui.car_var.set(available_cars[0])
    else:
        ui.car_var.set("")


def build_excel_options(ui):
    car_label = ttk.Label(ui.option_table, text="Car:")
    car_label.grid(row=0, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)

    ui.car_combo = ttk.Combobox(
        ui.option_table,
        textvariable=ui.car_var,
        state="readonly"
    )
    ui.car_combo.grid(row=0, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)

    update_car_combo_values(ui)

    start_label = ttk.Label(ui.option_table, text="Start Date:")
    start_label.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)

    start_entry = ttk.Entry(ui.option_table, textvariable=ui.start_date)
    start_entry.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)

    end_label = ttk.Label(ui.option_table, text="End Date:")
    end_label.grid(row=2, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)

    end_entry = ttk.Entry(ui.option_table, textvariable=ui.end_date)
    end_entry.grid(row=2, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)

    submit_button = ttk.Button(
        ui.option_table,
        text="Generate Report",
        command=lambda: excel_export(ui)
    )
    submit_button.grid(row=3, columnspan=2, padx=ENTRY_X, pady=ENTRY_Y)


def validate_inputs(ui):
    if not ui.is_valid_date(ui.start_date.get()):
        messagebox.showerror(
            "Date Error",
            "The Start date is not valid.\nUse YYYY-MM-DD."
        )
        return False

    if not ui.is_valid_date(ui.end_date.get()):
        messagebox.showerror(
            "Date Error",
            "The End date is not valid.\nUse YYYY-MM-DD."
        )
        return False

    start_date = datetime.strptime(ui.start_date.get(), "%Y-%m-%d").date()
    end_date = datetime.strptime(ui.end_date.get(), "%Y-%m-%d").date()

    if start_date > end_date:
        messagebox.showerror(
            "Date Error",
            "The start date must be before the end date."
        )
        return False

    return True

# * Export


def excel_export(ui):
    carId = next(
        (
            car["CarId"]
            for car in ui.cars
            if f"{car['Year']} {car['Make']} {car['Model']}" == ui.car_var.get()
        ),
        None
    )
    raw_data = calculate_mileage_pairs(ui.db.get_mileage_in_date_range(
        carId, ui.start_date.get(), ui.end_date.get()))

    monthly_miles = defaultdict(float)

    for entry in raw_data:
        end_date = datetime.strptime(entry["Date"], "%Y-%m-%d").date()
        start_date = end_date - timedelta(days=entry["Days"] - 1)

        miles_per_day = entry["Miles"] / entry["Days"]

        current_date = start_date

        while current_date <= end_date:
            month_key = current_date.strftime("%Y-%m")
            monthly_miles[month_key] += miles_per_day
            current_date += timedelta(days=1)

    monthly_miles = {
        month: round(miles)
        for month, miles in monthly_miles.items()
    }

    month_data = [
        {
            "Month": month,
            "Miles": miles
        }
        for month, miles in sorted(monthly_miles.items())
    ]

    today = date.today()
    with xlsxwriter.Workbook(f'Reports/Mileage Report {today.strftime("%m-%d-%Y")}.xlsx') as workbook:
        cell_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter"})

        car = ui.db.get_car_by_ID(1)
        # * Month Data
        month_wb = workbook.add_worksheet("Month")

        month_wb.set_column('A:D', 12)
        month_wb.merge_range(
            'A1:D1', f'{car["Year"]} {car["Make"]} {car["Model"]} {car["Trim"] or ""}', cell_format)
        month_wb.write('B2', 'Miles Driven', cell_format)
        month_wb.write('C2', 'Month', cell_format)

        row_num = 3
        for entry in month_data:
            month_wb.write(f'B{row_num}', entry["Miles"], cell_format)
            month_wb.write(f'C{row_num}', entry["Month"], cell_format)
            row_num += 1

        # * Raw Data
        raw_wb = workbook.add_worksheet("Raw")
        raw_wb.set_column('A:D', 12)
        raw_wb.merge_range(
            'A1:D1', f'{car["Year"]} {car["Make"]} {car["Model"]} {car["Trim"] or ""}', cell_format)
        raw_wb.write('B2', 'Miles Driven', cell_format)
        raw_wb.write('C2', 'Month', cell_format)

        row_num = 3
        for entry in raw_data:
            raw_wb.write(f'B{row_num}', entry["Miles"], cell_format)
            raw_wb.write(f'C{row_num}', entry["Date"], cell_format)
            row_num += 1

        raw_chart = workbook.add_chart({"type": "line"})

        raw_chart.add_series({
            "name": "Raw Data",
            "categories": f"='Raw'!$C$3:$C${row_num}",
            "values": f"='Raw'!$B$3:$B${row_num}",
            "data_labels": {
                "value": True,
            },
        })

        month_chart = workbook.add_chart({"type": "column"})

        month_chart.add_series({
            "name": "Month Data",
            "categories": f"='Month'!$C$3:$C${row_num}",
            "values": f"='Month'!$B$3:$B${row_num}",
            "data_labels": {
                "value": True,
            },
        })

        month_wb.insert_chart("F3", raw_chart)
        month_wb.insert_chart("F21", month_chart)

        raw_chart = workbook.add_chart({"type": "line"})

        raw_chart.add_series({
            "name": "Raw Data",
            "categories": f"='Raw'!$C$3:$C${row_num}",
            "values": f"='Raw'!$B$3:$B${row_num}",
        })

        month_chart = workbook.add_chart({"type": "column"})

        month_chart.add_series({
            "name": "Month Data",
            "categories": f"='Month'!$C$3:$C${row_num}",
            "values": f"='Month'!$B$3:$B${row_num}",
            "data_labels": {
                "value": True,
            },
        })

        raw_wb.insert_chart("F3", raw_chart)
        raw_wb.insert_chart("F21", month_chart)

    messagebox.showinfo("Report Ready", "Report has Been saved")
    ui.show_reports_screen()
