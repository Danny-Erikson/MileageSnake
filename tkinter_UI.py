import tkinter as tk
from tkinter import ttk

class Service_UI:
    def __init__(self, master, db):
        self.master = master
        master.title("Mileage Snake")
        master.geometry("500x500")
        master.protocol("WM_DELETE_WINDOW", self._on_close)

        self.db = db

        #Runtime
        self._show_main_screen()
    
    #* Builders

    def _show_main_screen(self):
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        title_label = tk.Label(self.master, text="Service Logger", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=25)

        mileage_button = ttk.Button(self.master, text="Enter Mileage", command="")
        mileage_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        service_button = ttk.Button(self.master, text="Service Entering", command="")
        service_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        man_cars_button = ttk.Button(self.master, text="Manage cars", command="")
        man_cars_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        man_services_button = ttk.Button(self.master, text="Manage recurring services")
        man_services_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        gen_report = ttk.Button(self.master, text="Generate Service Report")
        gen_report.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    #* Helper functions

    def _on_close(self):
        self.master.destroy()