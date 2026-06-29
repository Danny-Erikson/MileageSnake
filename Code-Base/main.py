import tkinter as tk

from pathlib import Path

from database import DB
from modules.UI_elements.tkinter_UI import Service_UI
from backup_routine import back_routine

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "Data" / "Cars.db"


def main():
    db = DB(DB_PATH)
    root = tk.Tk()
    Service_UI(root, db)
    root.mainloop()
    back_routine()


if __name__ == "__main__":
    main()
