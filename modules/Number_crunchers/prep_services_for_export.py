from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

def prep_services_for_export(service, latest_mileage ,avg_miles_per_day):
    packed = {}
    
    #* Name
    packed["Name"] = service["Name"]
    
    #* Mileage
    packed["MileageDoneAt"] = service["ServiceMileage"]
    packed["DueEveryMileage"] = service["MileageInterval"]
    packed["NextServiceMiles"] = service["ServiceMileage"] + service["MileageInterval"]
    
    #* Days and Dates
    service_date = datetime.strptime(service["ServiceDate"], "%Y-%m-%d").date()
    
    if service["DateUnit"] == "days":
        due_date = service_date + relativedelta(days=service["DateValue"])
    elif service["DateUnit"] == "months":
        due_date = service_date + relativedelta(months=service["DateValue"])
    elif service["DateUnit"] == "years":
        due_date = service_date + relativedelta(years=service["DateValue"])
    else:
        due_date = None
    
    if due_date != None:
        packed["DueDate"] = due_date.strftime("%m/%d/%Y")
    else:
        packed["DueDate"] = None
    
    #* Estimated Date
    days_mileage = math.ceil((packed["NextServiceMiles"] - latest_mileage["OdometerReading"]) / avg_miles_per_day)
    mileage_date = datetime.strptime(latest_mileage["Date"], "%Y-%m-%d").date() + relativedelta(days=days_mileage)
    packed["EstDate"] = min(mileage_date, due_date).strftime("%m/%d/%Y")
    
    return packed
