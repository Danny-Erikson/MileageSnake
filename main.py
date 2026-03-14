import tkinter as tk

from database import DB
from tkinter_UI import Service_UI

def main():
    db = DB(':memory:')

    root = tk.Tk()
    app = Service_UI(root, db)
    root.mainloop()


if __name__ == "__main__":
    main()
