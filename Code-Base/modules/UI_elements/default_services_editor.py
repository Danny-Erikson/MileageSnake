import tkinter as tk
from tkinter import ttk, messagebox

from modules.UI_elements.ui_padding import *


def show_default_services_editor(ui):
    # * Initialize Frame
    ui.clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    ui.master.columnconfigure(2, weight=1)
    ui.master.columnconfigure(3, weight=1)
    ui.master.columnconfigure(4, weight=1)

    # * Top of screen
    title_label = tk.Label(
        ui.master, text="Default Services", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=5, pady=TITLE_Y)

    top_text = tk.Label(
        ui.master, text="Below are the services that will be auto generated when a new car is added.")
    top_text.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

    # *Non Optional Table
    auto_service = ui.db.get_auto_temp_services()

    # * Building Table
    row_count = 2
    for service in auto_service:
        edit_button = tk.Button(
            ui.master,
            text="🖉",
            command=lambda templateId=service["TemplateId"]: show_service_form(
                ui, editing=True, templateId=templateId)
        )
        edit_button.grid(row=row_count, column=0, sticky="ew")

        service_name = tk.Label(ui.master, text=service["Name"])
        service_name.grid(row=row_count, column=1, sticky="ew")

        service_in_miles = tk.Label(
            ui.master, text=f"{service["DueMileage"]:,}" if service["DueMileage"] is not None else "")
        service_in_miles.grid(row=row_count, column=2, sticky="ew")

        service_in_days = tk.Label(
            ui.master, text=f"{day_formatter(service["IntervalValue"], service["IntervalUnit"])}" if service["IntervalValue"] is not None else "")
        service_in_days.grid(row=row_count, column=3, sticky="ew")

        remove_service_button = tk.Button(
            ui.master,
            text="Remove Service",
            command=lambda templateId=service["TemplateId"]: remove_service(
                ui, templateId=templateId)
        )
        remove_service_button.grid(row=row_count, column=4, sticky="ew")

        row_count += 1

    # *Optional table
    row_count += 1
    bottom_text = tk.Label(
        ui.master, text="Below are the services that the user is asked if they want to add.")
    bottom_text.grid(row=row_count, column=0, columnspan=5, padx=10, pady=10)

    asking_service = ui.db.get_asking_temp_services()

    # * Building Table
    row_count += 1
    for service in asking_service:
        edit_button = tk.Button(
            ui.master,
            text="🖉",
            command=lambda templateId=service["TemplateId"]: show_service_form(
                ui, editing=True, templateId=templateId)
        )
        edit_button.grid(row=row_count, column=0, sticky="ew")

        service_name = tk.Label(ui.master, text=service["Name"])
        service_name.grid(row=row_count, column=1, sticky="ew")

        service_in_miles = tk.Label(
            ui.master, text=f"{service["DueMileage"]:,}" if service["DueMileage"] is not None else "")
        service_in_miles.grid(row=row_count, column=2, sticky="ew")

        service_in_days = tk.Label(
            ui.master, text=f"{day_formatter(service["IntervalValue"], service["IntervalUnit"])}" if service["IntervalValue"] is not None else "")
        service_in_days.grid(row=row_count, column=3, sticky="ew")

        remove_service_button = tk.Button(
            ui.master,
            text="Remove Service",
            command=lambda templateId=service["TemplateId"]: remove_service(
                ui, templateId=templateId)
        )
        remove_service_button.grid(row=row_count, column=4, sticky="ew")

        row_count += 1

    # * Bottom of screen
    add_new = tk.Button(ui.master, text="Add New Service",
                        command=lambda: show_service_form(ui))
    add_new.grid(row=row_count, column=0, columnspan=5,
                 padx=BUTTON_X, pady=BUTTON_Y)
    go_back = tk.Button(ui.master, text="Go Back",
                        command=ui.show_advanced_area)
    go_back.grid(row=row_count + 1, column=0, columnspan=5,
                 padx=BUTTON_X, pady=BUTTON_Y)


def show_service_form(ui, templateId=None, editing=False):
    # * Initialize frame
    ui.clear_frame()
    ui.master.columnconfigure(0, weight=1)
    ui.master.columnconfigure(1, weight=1)
    ui.master.columnconfigure(2, weight=1)

    ui.name_var = tk.StringVar()
    ui.due_mileage_var = tk.StringVar()
    ui.time_value_var = tk.StringVar()
    ui.time_unit_var = tk.StringVar()
    ui.optional_var = tk.BooleanVar()
    ui.question_var = tk.StringVar()

    # * Conditional rendering
    # The editing flag is True if the user clicked the edit button to call the function
    # if so change the title of the frame and pass in DB data from the service ID
    # also change the function called when we click the submit button
    if editing:
        title_label = ttk.Label(
            ui.master, text="Edit Service", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=3, pady=TITLE_Y)

        # call db for values
        service = ui.db.get_services_temp_by_id(templateId)

        ui.name_var.set(value=service["Name"])
        ui.due_mileage_var.set(value=service["DueMileage"] or "")
        ui.time_value_var.set(value=service["IntervalValue"] or "")
        ui.time_unit_var.set(value=service["IntervalUnit"] or "")
        ui.optional_var.set(
            value=True if service["IsOptional"] == 1 else False)
        ui.question_var.set(value=service["Question"] or "")

        submit_button = ttk.Button(
            ui.master, text="Submit", command=lambda templateId=service["TemplateId"]: edit_service(ui, templateId))
        submit_button.grid(row=7, columnspan=3, padx=BUTTON_X, pady=BUTTON_Y)

    else:
        title_label = ttk.Label(
            ui.master, text="Add a New Service", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=3, pady=TITLE_Y)

        submit_button = ttk.Button(
            ui.master, text="Submit", command=lambda: add_service(ui))
        submit_button.grid(row=7, columnspan=3, padx=BUTTON_X, pady=BUTTON_Y)

    # * Building of Shared Elements

    name_label = ttk.Label(ui.master, text="Name:")
    name_label.grid(row=1, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    name_entry = ttk.Entry(ui.master, textvariable=ui.name_var)
    name_entry.grid(row=1, column=1, sticky="we", padx=ENTRY_X, pady=ENTRY_Y)

    mileage_label = ttk.Label(ui.master, text="Due Mileage:")
    mileage_label.grid(row=2, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    mileage_entry = ttk.Entry(ui.master, textvariable=ui.due_mileage_var,
                              validate="key", validatecommand=(ui.int_vcmd, "%P"))
    mileage_entry.grid(row=2, column=1, sticky="we",
                       padx=ENTRY_X, pady=ENTRY_Y)

    time_label = ttk.Label(ui.master, text="Due Every:")
    time_label.grid(row=3, column=0, sticky="e", padx=ENTRY_X, pady=ENTRY_Y)
    time_entry = ttk.Entry(ui.master, textvariable=ui.time_value_var,
                           validate="key", validatecommand=(ui.int_vcmd, "%P"))
    time_entry.grid(row=3, column=1, sticky="we", padx=ENTRY_X, pady=ENTRY_Y)
    time_combo = ttk.Combobox(
        ui.master, textvariable=ui.time_unit_var, state="readonly")
    time_combo["values"] = ["days", "months", "years"]
    time_combo.grid(row=3, column=2, sticky="w", padx=ENTRY_X, pady=ENTRY_Y)

    ask_checkbox = tk.Checkbutton(ui.master, text="Ask to Create (for services that apply to some car)",
                                  variable=ui.optional_var, command=lambda: question_toggle(ui))
    ask_checkbox.grid(row=4, columnspan=3, padx=ENTRY_X, pady=ENTRY_Y)

    question_label = ttk.Label(ui.master, text="Question:")
    question_label.grid(row=5, column=0, sticky="e",
                        padx=ENTRY_X, pady=ENTRY_Y)
    ui.question_entry = ttk.Entry(ui.master, textvariable=ui.question_var)
    ui.question_entry.grid(row=5, column=1, columnspan=2,
                           sticky="we", padx=ENTRY_X, pady=ENTRY_Y)

    question_toggle(ui)

    question_instr = question_label = ttk.Label(
        ui.master, text="When a new car is added, a messagebox with that question will pop up.\nMake sure the question can be answered with Yes or No")
    question_instr.grid(row=6, columnspan=3)

    back_button = ttk.Button(ui.master, text="Go Back",
                             command=lambda: show_default_services_editor(ui))
    back_button.grid(row=8, columnspan=3, padx=BUTTON_X, pady=BUTTON_Y)


def validate_inputs(ui):
    if ui.name_var.get() == "":
        messagebox.showerror("Input Error", "Name can not be blank")
        return False

    if ui.due_mileage_var.get() == "" and ui.time_value_var.get() == "":
        messagebox.showerror(
            "Input Error", "Mileage Due and Due every cannot both be blank\nOne or both must be filled")
        return False

    if ui.time_value_var.get() != "" and ui.time_unit_var.get() == "":
        messagebox.showerror("Input Error", "Select a timeframe from the box")
        return False

    if ui.optional_var.get() == True and ui.question_var.get() == "":
        messagebox.showerror(
            "Input Error", "Question cannot be blank for a optional service")
        return False

    return True


def add_service(ui):
    if not validate_inputs(ui):
        return

    good_inputs = (ui.name_var.get(), ui.due_mileage_var.get() or None)

    if ui.time_value_var.get() == "":
        safe_inputs = (*good_inputs, None, None)
    else:
        safe_inputs = (*good_inputs, ui.time_value_var.get(),
                       ui.time_unit_var.get())

    sanitized_inputs = (*safe_inputs, 1 if ui.optional_var.get() else 0)

    ui.db.add_services_template(
        *sanitized_inputs, ui.question_var.get() if ui.optional_var.get() else "")

    show_default_services_editor(ui)


def edit_service(ui, templateId):
    if not validate_inputs(ui):
        return

    good_inputs = (ui.name_var.get(), ui.due_mileage_var.get() or None)

    if ui.time_value_var.get() == "":
        safe_inputs = (*good_inputs, None, None)
    else:
        safe_inputs = (*good_inputs, ui.time_value_var.get(),
                       ui.time_unit_var.get())

    sanitized_inputs = (*safe_inputs, 1 if ui.optional_var.get() else 0)

    ui.db.update_services_template(
        *sanitized_inputs, ui.question_var.get() if ui.optional_var.get() else "", templateId)

    show_default_services_editor(ui)


def remove_service(ui, templateId):
    service = ui.db.get_services_temp_by_id(templateId)
    confirmed = messagebox.askyesno(
        "Delete Service", f"Are you sure you want to delete {service["Name"]}")
    if confirmed:
        ui.db.remove_services_template(templateId)
        show_default_services_editor(ui)


def day_formatter(value, unit):
    if value == 1:
        return f"{value} {unit[:-1]}"
    else:
        return f"{value} {unit}"


def question_toggle(ui):
    if ui.optional_var.get():
        ui.question_entry.config(state="normal")
    else:
        ui.question_entry.config(state="disabled")
