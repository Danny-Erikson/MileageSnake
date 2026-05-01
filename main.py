import tkinter as tk

from database import DB
from tkinter_UI import Service_UI

def main():
#TODO: TEST going from screen to screen with stuff on each screen with shared variables

    db = DB('Data/Cars.db')
    root = tk.Tk()
    Service_UI(root, db)
    root.mainloop()


if __name__ == "__main__":
    main()
