def calculate_MPG_data(fuel_data):
    # *Data Setup
    export = []
    last_mileage = fuel_data[0]["OdometerReading"]
    fuel_data.pop(0)
    gallons = 0
    cost = 0
    data = {}

    # * Calculate Data
    for entry in fuel_data:
        if entry["FullFillUp"] == 0:
            gallons += entry["GallonsBought"]
            cost += entry["TotalCost"]
        else:
            gallons += entry["GallonsBought"]
            cost += entry["TotalCost"]

            # *MPG calculation
            mileage = entry["OdometerReading"] - last_mileage
            mpg = int((mileage / gallons) * 100) / 100

            # *Cost per Gallon Calculation
            cpg = int((cost / gallons) * 100) / 100

            # *Cost per mile Calculation
            cpm = int((cost / mileage) * 100) / 100

            # *Pack Data
            data = {
                "MPG": mpg,
                "CPG": cpg,
                "CPM": cpm,
                "Date": entry["Date"]
            }
            export.append(data)

            # *Reset before next iteration
            last_mileage = entry["OdometerReading"]
            gallons = 0
            cost = 0
    return export
