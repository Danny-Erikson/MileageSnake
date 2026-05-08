from datetime import datetime

def calculate_mileage_pairs(reading_data):
    """
    Calculate mileage and day differences between consecutive mileage records.
    
    Args:
        reading_data (list[dict]): A list of mileage records. Each record should
            contain:
                - "OdometerReading" (int): The odometer reading.
                - "Date" (str): The date of the reading in YYYY-MM-DD format.
    
    Returns:
        list[dict]: A list of dictionaries where each dictionary contains:
            - "Miles" (int): Difference in odometer readings between two records.
            - "Days" (int): Difference in days between the two dates.
            - "Date" (str): The date of the newer mileage record.
    """
    
    data = []
    
    for i in range(len(reading_data) - 1):
        mileage1 = reading_data[i]
        mileage2 = reading_data[i + 1]
        
        mile_diff = mileage2["OdometerReading"] - mileage1["OdometerReading"]
        
        day_diff = (
            datetime.strptime(mileage2["Date"], "%Y-%m-%d").date()
            - datetime.strptime(mileage1["Date"], "%Y-%m-%d").date()
        ).days
        
        packed = {
            "Miles": mile_diff,
            "Days": day_diff,
            "Date": mileage2["Date"]
        }
        
        data.append(packed)
    
    return data
