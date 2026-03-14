import sqlite3

#* Database calls go here and the functions are called in the UI 

SCHEMA = """
CREATE TABLE IF NOT EXISTS Cars (
    CarId INTEGER PRIMARY KEY AUTOINCREMENT,
    VINNumber TEXT,
    LicensePlate TEXT,
    Year INT NOT NULL,
    Make TEXT NOT NULL,
    Model TEXT NOT NULL,
    Trim TEXT
);

CREATE TABLE IF NOT EXISTS Mileage (
    MileageId INTEGER PRIMARY KEY AUTOINCREMENT,
    CarID INT,
    OdometerReading INT NOT NULL,
    Date TEXT NOT NULL,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID)
);

CREATE TABLE IF NOT EXISTS RecurringServices(
    ServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    CarID INT,
    DueMileage INTEGER NOT NULL,
    DueDays INTEGER NOT NULL,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID)
);

CREATE TABLE IF NOT EXISTS ServicesDone(
    CarServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    CarID INT,
    ServiceId INT,
    MileageId INT,
    Description TEXT,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID),
    FOREIGN KEY (ServiceId) REFERENCES RecurringServices(ServiceId),
    FOREIGN KEY (MileageId) REFERENCES Mileage(MileageId)
);
"""

class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

        self.conn.executescript(SCHEMA)
    
    def close(self):
        self.conn.close()
    
    #* DB Helper
    def execute(self, sql, params = ()):
        with self.conn:
            cur = self.conn.execute(sql, params)
        return cur
    
    #? We have these fetch functions as it makes it easier to call results
    #? The return is closer to a object notation
    
    def fetchone(self, sql, params = ()):
        cur = self.conn.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None
    
    def fetchall(self, sql, params = ()):
        cur = self.conn.execute(sql, params)
        rows = cur.fetchall() 
        return [dict(row) for row in rows]
    
    #* Cars
    def add_car(self, vin, plate, year, make, model, trim):
        self.execute(
            """
            INSERT INTO Cars (VINNumber, LicensePlate, Year, Make, Model, Trim)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (vin, plate, year, make, model, trim),
        )
    
    def get_all_cars(self):
        return self.fetchall("SELECT * FROM Cars")