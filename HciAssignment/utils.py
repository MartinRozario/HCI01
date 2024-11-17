import sys
from tkinter import messagebox

def handle_error(e):
    """Global error handler function."""
    messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    sys.exit(1)  # Exit the program immediately