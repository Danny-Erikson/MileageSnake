import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

import xlsxwriter

from modules.HTML_Builders.title_card import build_title_card
from modules.HTML_Builders.serivce_card import build_service_card

from ui_padding import *


def show_service_done_config(ui):
    # * Initialize Frame
    ui.clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)

    ui.car_var = tk.StringVar()
    ui.type_var = tk.StringVar(value="HTML")
    ui.display_var = tk.StringVar()

    # * Top of the screen
    title_label = tk.Label(
        ui.master, text="Services Done Report", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=TITLE_Y)

    # * Middle of the screen
    html_radio = ttk.Radiobutton(
        ui.master, text="HTML", variable=ui.type_var, value="HTML", command=lambda: on_type_change(ui))
    html_radio.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)

    excel_radio = ttk.Radiobutton(
        ui.master, text="Excel", variable=ui.type_var, value="Excel", command=lambda: on_type_change(ui))
    excel_radio.grid(row=1, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)

    ui.option_table = tk.Frame(ui.master)
    ui.option_table.grid(row=2, column=0, columnspan=2, sticky="ew")
    ui.option_table.columnconfigure(0, weight=1)
    ui.option_table.columnconfigure(1, weight=1)

    on_type_change(ui)

    # * Bottom of screen
    back_button = ttk.Button(ui.master, text="Go Back",
                             command=ui.show_reports_screen)
    back_button.grid(row=3, columnspan=2, padx=BUTTON_X, pady=BUTTON_Y)


def on_type_change(ui):
    # *Table Clean Up
    for widget in ui.option_table.winfo_children():
        widget.destroy()

    if ui.type_var.get() == "Excel":
        build_excel_options(ui)
    else:
        build_html_options(ui)


def build_shared_options(ui):
    car_label = ttk.Label(ui.option_table, text="Car:")
    car_label.grid(row=0, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)

    ui.car_combo = ttk.Combobox(
        ui.option_table, textvariable=ui.car_var, state="readonly")
    ui.car_combo["values"] = ["ALL"] + \
        [f"{c['Year']} {c['Make']} {c['Model']}" for c in ui.cars]
    ui.car_var.set(ui.car_combo["values"][ui.car_index])
    ui.car_combo.grid(row=0, column=1, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)


def build_excel_options(ui):
    build_shared_options(ui)

    submit_button = ttk.Button(
        ui.option_table, text="Generate Report", command=lambda: excel_export(ui))
    submit_button.grid(row=1, columnspan=2, padx=ENTRY_X, pady=ENTRY_Y)


def build_html_options(ui):
    build_shared_options(ui)

    submit_button = ttk.Button(
        ui.option_table, text="Generate Report", command=lambda: html_export(ui))
    submit_button.grid(row=2, columnspan=2, padx=ENTRY_X, pady=ENTRY_Y)


def html_export(ui):
    if ui.car_var.get() == "ALL":
        cars = [car["CarId"] for car in ui.cars]
    else:
        selected_car_text = ui.car_var.get()
        cars = [
            car["CarId"] for car in ui.cars
            if f"{car['Year']} {car['Make']} {car['Model']}" == selected_car_text
        ]

    today = date.today()
    for car_id in cars:
        car = ui.db.get_car_by_ID(car_id)
        with open(f'Reports/Services Due Report {car["Model"]} {today.strftime("%m-%d-%Y")}.html', "w") as doc:
            doc.write("""<!doctype html>
    <html>
    <head>
        <style>
        .card {
            padding: 10px;
            border-radius: 15px;
            margin: 10px;
        }
        .reoccurring {
            background-color: rgba(119, 136, 153, 0.5);
        }
        .general {
            background-color: rgba(187, 119, 82, 0.5);
        }
        .flex-container {
            display: flex;
            justify-content: space-between;
            padding-bottom: 3px;
            font-size: 16px;
        }
        .flex-item {
            font-size: 24px;
            font-weight: bold;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
        }
        .notes {
            font-size: 24px;
            font-weight: bold;
        }
        .smaller {
            padding: 2px 6px;
            font-size: 0.7em;
            font-style: italic;
            font-weight: initial;
        }
        </style>
    </head>
    <body>
    """)
            build_title_card(doc, car, ui.text_color_for_bg(car["Color"]))
            build_service_card(doc, ui.db.get_service_report_data(car_id))
            doc.write("""  </body>
    </html>""")
    messagebox.showinfo("Report Ready", "Report has Been saved")
    ui.show_reports_screen()


def excel_export(ui):
    if ui.car_var.get() == "ALL":
        cars = [car["CarId"] for car in ui.cars]
    else:
        selected_car_text = ui.car_var.get()
        cars = [
            car["CarId"] for car in ui.cars
            if f"{car['Year']} {car['Make']} {car['Model']}" == selected_car_text
        ]

    today = date.today()
    with xlsxwriter.Workbook(f'Reports/Services Done Report {today.strftime("%m-%d-%Y")}.xlsx') as workbook:
        cell_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter"})

        num_format = workbook.add_format({
            "num_format": "#,##0"})

        date_format = workbook.add_format({
            "num_format": "mm/dd/yy",
            "align": "right"})

        for car_id in cars:
            car = ui.db.get_car_by_ID(car_id)
            # * Crate workbook
            worksheet = workbook.add_worksheet(car["Model"])
            worksheet.merge_range(
                'A1:F1', f'{car["Year"]} {car["Make"]} {car["Model"]} {car["Trim"] or ""}', cell_format)

            worksheet.merge_range(
                'A2:B2', "Service", cell_format)
            worksheet.merge_range(
                'C2:D2', "Mileage", cell_format)
            worksheet.merge_range(
                'E2:F2', "Date", cell_format)

            data = ui.db.get_service_report_data(car_id)
            print(data)
            col_num = 3
            for entry in data:
                worksheet.merge_range(
                    f'A{col_num}:B{col_num}', entry["Name"])
                worksheet.merge_range(
                    f'C{col_num}:D{col_num}', entry["ServiceMileage"], num_format)
                worksheet.merge_range(
                    f'E{col_num}:F{col_num}', entry["ServiceDate"], date_format)
                col_num += 1

    messagebox.showinfo("Report Ready", "Report has Been saved")
    ui.show_reports_screen()
