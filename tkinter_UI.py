import tkinter as tk
from tkinter import ttk

class Service_UI:
    def __init__(self, master, db):
        self.master = master
        master.title("Mileage Snake")
        master.geometry("600x500")
        master.protocol("WM_DELETE_WINDOW", self._on_close)

        self.db = db

        #Runtime
        self._show_main_screen()
    
    #* Builders

    #* Main Screen

    def _show_main_screen(self):
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        title_label = tk.Label(self.master, text="Service Logger", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=25)

        mileage_button = ttk.Button(self.master, text="Enter Mileage", command="")
        mileage_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        service_button = ttk.Button(self.master, text="Service Entering", command="")
        service_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        man_cars_button = ttk.Button(self.master, text="Manage cars", command=self._show_car_manager)
        man_cars_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        man_services_button = ttk.Button(self.master, text="Manage recurring services")
        man_services_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        gen_report = ttk.Button(self.master, text="Generate Service Report")
        gen_report.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    #* Car Manager

    def _show_car_manager(self):
        #TODO: Add new Car Button fictionally
        #TODO: Edit Button fictionally
        #TODO: Remove button fictionally
        # Clear Frame
        self._clear_frame()
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=1)


        cars = self.db.get_all_cars()

        title_label = tk.Label(self.master, text="Cars", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=5, pady=25)

        car_label = tk.Label(self.master, text="Car")
        car_label.grid(row=1, column=1, sticky="ew")
        license_label = tk.Label(self.master, text="License plate")
        license_label.grid(row=1, column=2, sticky="ew")
        vin_label = tk.Label(self.master, text="VIN Number")
        vin_label.grid(row=1, column=3, sticky="ew")
        
        # This for loop is to build a table based on the number of entry in the cars table
        # The .bind on each element to allow the text to be copyable 
        row_count = 2
        for car in cars:
            edit_button = tk.Button(self.master, text="🖉")
            edit_button.grid(row=row_count, column=0, sticky="ew")
            car_name = tk.Label(self.master, text=f"{car["Year"]} {car["Make"]} {car["Model"]} {car["Trim"] or ""}")
            car_name.bind("<Button-1>", self.copy_text)
            car_name.grid(row=row_count, column=1, sticky="ew")
            car_vin = tk.Label(self.master, text=car["LicensePlate"])
            car_vin.bind("<Button-1>", self.copy_text)
            car_vin.grid(row=row_count, column=2, sticky="ew")
            car_license = tk.Label(self.master, text=car["VINNumber"])
            car_license.bind("<Button-1>", self.copy_text)
            car_license.grid(row=row_count, column=3, sticky="ew")
            remove_car = tk.Button(self.master, text="Remove Car")
            remove_car.grid(row=row_count, column=4, sticky="ew")
            row_count += 1
        
        # Below the table elements
        copy_inst = tk.Label(self.master, text="Click on car values to copy to clipboard")
        copy_inst.grid(row=row_count + 1, column=0, columnspan=5, pady=10)
        add_new = tk.Button(self.master, text="Add New Car")
        add_new.grid(row=row_count + 2, column=0, columnspan=5, pady=10)
        go_back = tk.Button(self.master, text="Go Back", command=self._show_main_screen)
        go_back.grid(row=row_count + 3, column=0, columnspan=5, pady=10)


    #* Helper functions

    def _on_close(self):
        self.master.destroy()
    
    def _clear_frame(self):
        #clears elements
        for widget in self.master.winfo_children():
            widget.destroy()
        # Reset column/row weight
        for i in range(10):
            self.master.columnconfigure(i, weight=0)
            self.master.rowconfigure(i, weight=0)

    def copy_text(self, event):
        self.master.clipboard_clear()
        self.master.clipboard_append(event.widget["text"])

        msg = ttk.Label(self.master, text="Copied!")
        msg.place(x=event.x_root - self.master.winfo_rootx(),
                y=event.y_root - self.master.winfo_rooty())
        self.master.after(800, msg.destroy)