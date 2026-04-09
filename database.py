import sqlite3

#TODO: fix CarID to CarId

SCHEMA = """
CREATE TABLE IF NOT EXISTS Cars (
    CarID INTEGER PRIMARY KEY AUTOINCREMENT,
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

CREATE TABLE IF NOT EXISTS FuelLog (
    FuelLogId INTEGER PRIMARY KEY AUTOINCREMENT,
    MileageId INTEGER NOT NULL UNIQUE,
    GallonsBought REAL NOT NULL,
    TotalCost REAL NOT NULL,
    FullFillUp INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (MileageId) REFERENCES Mileage(MileageId)
);

CREATE TABLE IF NOT EXISTS RecurringServices(
    ServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    CarID INT,
    DueMileage INTEGER,
    DueDays INTEGER,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID)
    CHECK (NOT (DueMileage IS NULL AND DueDays IS NULL))
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
            return cur.lastrowid
    
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
            (vin, plate, year, make, model, trim)
        )
    
    def get_all_cars(self):
        return self.fetchall("SELECT * FROM Cars")
    
    def get_car_by_ID(self, carID):
        return self.fetchone("SELECT * FROM Cars WHERE CarID = ?", (carID,))
    
    def update_car(self, vin, plate, year, make, model, trim, car_id):
        self.execute(
            """
            UPDATE Cars
            SET VINNumber = ?, LicensePlate = ?, Year = ?, Make = ?, Model = ?, Trim = ?
            WHERE CarID = ?
            """,
            (vin, plate, year, make, model, trim, car_id)
        )
    
    def remove_car(self, carID):
        self.execute("DELETE FROM Cars WHERE CarID = ?", (carID,))
    
    #* Mileage
    def add_mileage(self, carID, reading, date):
        mileageID = self.execute(
            """
            INSERT INTO Mileage (CarID, OdometerReading, Date)
            VALUES (?, ?, ?)
            """,
            (carID, reading, date)
        )
        return mileageID
    
    def get_mileage_by_ID(self, carID):
        return self.fetchone("SELECT * FROM Mileage WHERE CarID = ?", (carID,))
    
    def add_fuel(self, mileageID, gallonsBrought, totalCost, fullFillUp):
        self.execute(
            """
            INSERT INTO FuelLog (MileageID, GallonsBought, TotalCost, FullFillUp)
            VALUES (?, ?, ?, ?)
            """,
            (mileageID, gallonsBrought, totalCost, fullFillUp)
        )
    
    #* Recurring Services
    def add_recurring_services(self, name, carID, dueMileage, dueDays):
        self.execute(
            """
            INSERT INTO RecurringServices (Name, carID, DueMileage, DueDays)
            VALUES (?, ?, ?, ?)
            """,
            (name, carID, dueMileage , dueDays)
        )
    
    def get_recurring_services_by_ID(self, serviceID):
        return self.fetchone("SELECT * FROM RecurringServices WHERE serviceID = ?", (serviceID,))
    
    def get_recurring_services_by_carID(self, carID):
        return self.fetchall(("""SELECT *
                                FROM RecurringServices
                                WHERE CarID = ?
                                ORDER BY 
                                DueMileage IS NULL,
                                DueMileage ASC,
                                DueDays ASC;"""),
                                (carID,))
    
    def update_recurring_service(self, name, dueMileage, dueDays, service_id):
            self.execute(
                """
                UPDATE RecurringServices
                SET Name = ?, DueMileage = ?, DueDays = ?
                WHERE ServiceId = ?
                """,
                (name, dueMileage, dueDays, service_id)
            )
    
    def remove_recurring_service(self, service_id):
        self.execute("DELETE FROM RecurringServices WHERE ServiceId = ?", (service_id,))
    