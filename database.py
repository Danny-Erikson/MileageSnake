import sqlite3
from pathlib import Path

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
    CarId INT,
    OdometerReading INT NOT NULL,
    Date TEXT NOT NULL,
    FOREIGN KEY (CarId) REFERENCES Cars(CarId)
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
    CarId INT,
    DueMileage INTEGER,
    IntervalValue INTEGER,
    IntervalUnit TEXT CHECK (IntervalUnit IN ('days', 'months', 'years')),
    AutoNote TEXT,
    FOREIGN KEY (CarId) REFERENCES Cars(CarId),

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
    CarId INT,
    ServiceId INT,
    MileageId INT,
    Note TEXT,
    FOREIGN KEY (CarId) REFERENCES Cars(CarId),
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
        INSERT INTO RecurringServices (Name, CarId, DueMileage, IntervalValue, IntervalUnit)
        SELECT Name, ?, DueMileage, IntervalValue, IntervalUnit
        FROM ServiceTemplates
        WHERE IsOptional = 0;
        """,
        (car_id,))
        
        return car_id
    
    def get_all_cars(self):
        return self.fetchall("SELECT * FROM Cars")
    
    def get_car_by_ID(self, carID):
        return self.fetchone("SELECT * FROM Cars WHERE CarId = ?", (carID,))
    
    def update_car(self, vin, plate, year, make, model, trim, car_id):
        self.execute(
            """
            UPDATE Cars
            SET VINNumber = ?, LicensePlate = ?, Year = ?, Make = ?, Model = ?, Trim = ?
            WHERE CarId = ?
            """,
            (vin, plate, year, make, model, trim, car_id)
        )
    
    def remove_car(self, carID):
        self.execute("DELETE FROM Cars WHERE CarId = ?", (carID,))
    
    #* Mileage
    def add_mileage(self, carID, reading, date):
        mileageID = self.execute(
            """
            INSERT INTO Mileage (CarId, OdometerReading, Date)
            VALUES (?, ?, ?)
            """,
            (carID, reading, date)
        )
        return mileageID
    
    def get_mileage_by_ID(self, carID):
        return self.fetchone("SELECT * FROM Mileage WHERE CarId = ?", (carID,))
    
    def add_fuel(self, mileageID, gallonsBrought, totalCost, fullFillUp):
        self.execute(
            """
            INSERT INTO FuelLog (MileageID, GallonsBought, TotalCost, FullFillUp)
            VALUES (?, ?, ?, ?)
            """,
            (mileageID, gallonsBrought, totalCost, fullFillUp)
        )
    
    def mileage_match(self, carId, reading, date):
        return self.fetchone("SELECT * FROM Mileage WHERE CarId = ? AND OdometerReading = ? AND Date = ?", (carId, reading, date))
    
    #* Recurring Services
    def add_recurring_services(self, name, carID, dueMileage, intervalValue, intervalUnit, autoNote):
        self.execute(
            """
            INSERT INTO RecurringServices (Name, CarId, DueMileage, IntervalValue, IntervalUnit, AutoNote)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, carID, dueMileage , intervalValue, intervalUnit, autoNote)
        )
    
    def get_recurring_services_by_ID(self, serviceID):
        return self.fetchone("SELECT * FROM RecurringServices WHERE ServiceId = ?", (serviceID,))
    
    def get_recurring_services_by_carID(self, carID):
        return self.fetchall(("""SELECT *
                                FROM RecurringServices
                                WHERE CarId = ?
                                ORDER BY 
                                DueMileage ASC;"""),
                                (carID,))
    
    def update_recurring_service(self, name, dueMileage, intervalValue, intervalUnit, autoNote, service_id):
        self.execute(
            """
            UPDATE RecurringServices
            SET Name = ?, DueMileage = ?, IntervalValue = ?, intervalUnit = ?, AutoNote = ?
            WHERE ServiceId = ?
            """,
            (name, dueMileage, intervalValue, intervalUnit, autoNote, service_id)
        )
    
    def remove_recurring_service(self, service_id):
        self.execute("DELETE FROM RecurringServices WHERE ServiceId = ?", (service_id,))
    
    def update_auto_note_by_id(self, note, service_id):
        self.execute(
            """
            UPDATE RecurringServices
            SET AutoNote = ?
            WHERE ServiceId = ?
            """,
            (note, service_id)
        )
    
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
    
    #* Service Done
    def add_service(self, name, carId, serviceId, mileageId, note):
        self.execute(
            """
            INSERT INTO ServicesDone (Name, CarId, ServiceId, MileageId, Note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, carId, serviceId, mileageId, note)
        )