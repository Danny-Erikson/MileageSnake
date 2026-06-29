import tkinter as tk

from database import DB
from modules.UI_elements.tkinter_UI import Service_UI


def main():
    db = DB('Data/Cars.db')
    root = tk.Tk()
    Service_UI(root, db)
    root.mainloop()


if __name__ == "__main__":
    main()
