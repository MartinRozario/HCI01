import tkinter as tk
from utils import handle_error
from application import Application
from database import create_db

if __name__ == "__main__":
    try:
        create_db()
        root = tk.Tk()
        app = Application(root)
        root.mainloop()
    except Exception as e:
        handle_error(e)