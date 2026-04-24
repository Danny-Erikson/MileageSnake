import sqlite3
from pathlib import Path

#TODO: fix CarID to CarId
#TODO: Update ERD

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

CREATE TABLE IF NOT EXISTS ServiceTemplates (
    TemplateId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    DueMileage INTEGER,
    IntervalValue INTEGER,
    IntervalUnit TEXT CHECK (IntervalUnit IN ('days', 'months', 'years')),
    IsOptional INTEGER NOT NULL,
    Question TEXT
);

CREATE TABLE IF NOT EXISTS RecurringServices(
    ServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    CarID INT,
    DueMileage INTEGER,
    IntervalValue INTEGER,
    IntervalUnit TEXT CHECK (IntervalUnit IN ('days', 'months', 'years')),
    FOREIGN KEY (CarID) REFERENCES Cars(CarID),

    CHECK (
        DueMileage IS NOT NULL
        OR (IntervalValue IS NOT NULL AND IntervalUnit IS NOT NULL)
    ),

    CHECK (
        (IntervalValue IS NULL AND IntervalUnit IS NULL)
        OR (IntervalValue IS NOT NULL AND IntervalUnit IS NOT NULL)
    )
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
        db_path = Path(path)
        is_new_db = not db_path.exists()
        
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
        self.conn.executescript(SCHEMA)
        
        if is_new_db:
            self.conn.execute("""
            INSERT INTO ServiceTemplates 
                (Name, DueMileage, IntervalValue, IntervalUnit, IsOptional, Question)
            VALUES
                ('Oil change', 5000, 6, 'months', 0, NULL),
                ('Eng. Intake Filter', 15000, 1, 'years', 0, NULL),
                ('Cabin Air Filter', 15000, 1, 'years', 0, NULL),
                ('Coolant', 30000, 4, 'years', 0, NULL),
                ('Power Steering', 40000, 3, 'years', 0, NULL),
                ('Transmission Fluid', 60000, NULL, NULL, 0, NULL),
                ('Brake Fluid', 45000, 3, 'years', 0, NULL),
                ('Rear Differential Fluid', 60000, 5, 'years', 1, 'Does the car have a rear differential');
            """)
            
            self.conn.commit()
    
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
        car_id = self.execute(
            """
            INSERT INTO Cars (VINNumber, LicensePlate, Year, Make, Model, Trim)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (vin, plate, year, make, model, trim)
        )
        
        self.execute("""
        INSERT INTO RecurringServices (Name, CarID, DueMileage, IntervalValue, IntervalUnit)
        SELECT Name, ?, DueMileage, IntervalValue, IntervalUnit
        FROM ServiceTemplates
        WHERE IsOptional = 0;
        """,
        (car_id,))
        
        return car_id
    
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
    def add_recurring_services(self, name, carID, dueMileage, intervalValue, intervalUnit):
        self.execute(
            """
            INSERT INTO RecurringServices (Name, carID, DueMileage, IntervalValue, IntervalUnit)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, carID, dueMileage , intervalValue, intervalUnit)
        )
    
    def get_recurring_services_by_ID(self, serviceID):
        return self.fetchone("SELECT * FROM RecurringServices WHERE serviceID = ?", (serviceID,))
    
    def get_recurring_services_by_carID(self, carID):
        return self.fetchall(("""SELECT *
                                FROM RecurringServices
                                WHERE CarID = ?
                                ORDER BY 
                                DueMileage ASC;"""),
                                (carID,))
    
    def update_recurring_service(self, name, dueMileage, intervalValue, intervalUnit,  service_id):
            self.execute(
                """
                UPDATE RecurringServices
                SET Name = ?, DueMileage = ?, IntervalValue = ?, intervalUnit = ?
                WHERE ServiceId = ?
                """,
                (name, dueMileage, intervalValue, intervalUnit, service_id)
            )
    
    def remove_recurring_service(self, service_id):
        self.execute("DELETE FROM RecurringServices WHERE ServiceId = ?", (service_id,))
    
    #* Service Templates
    def add_services_template(self, name, dueMileage, intervalValue, intervalUnit, isOptional, question):
        self.execute(
            """
            INSERT INTO ServiceTemplates (Name, DueMileage, IntervalValue, IntervalUnit, IsOptional, Question)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, dueMileage, intervalValue, intervalUnit, isOptional, question)
        )
    
    def get_auto_temp_services(self):
        return self.fetchall("SELECT * FROM ServiceTemplates WHERE IsOptional = 0 ORDER BY DueMileage ASC")
    
    def get_asking_temp_services(self):
        return self.fetchall("SELECT * FROM ServiceTemplates WHERE IsOptional = 1 ORDER BY DueMileage ASC")
    
    def get_services_temp_by_id(self, templateId):
        return self.fetchone("SELECT * FROM ServiceTemplates  WHERE TemplateId = ?", (templateId,))
    
    def update_services_template(self, name, dueMileage, intervalValue, intervalUnit, isOptional, question, templateId):
            self.execute(
                """
                UPDATE ServiceTemplates
                SET Name = ?, DueMileage = ?, IntervalValue = ?, intervalUnit = ?, IsOptional = ?, Question = ?
                WHERE TemplateId = ?
                """,
                (name, dueMileage, intervalValue, intervalUnit, isOptional, question, templateId)
            )
    
    def remove_services_template(self, templateId):
        self.execute("DELETE FROM ServiceTemplates WHERE TemplateId = ?", (templateId,))