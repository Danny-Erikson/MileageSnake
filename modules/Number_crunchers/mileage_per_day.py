def calculate_mileage_per_day(mileage_days_pairs):
    """
    Calculate the average miles driven per day for each mileage record.
    
    Each item in mileage_days_pairs should be a dictionary containing:
        Miles: The number of miles driven.
        Days: The number of days over which those miles were driven.
    
    Returns:
        A list of daily mileage averages.
    """
    data = []
    
    for i in range(len(mileage_days_pairs)):
        mileage = mileage_days_pairs[i]
        avg = mileage["Miles"] / mileage["Days"]
        data.append(avg)
    
    return data
