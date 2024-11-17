import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import handle_error

class InstructorManagement:
    def __init__(self, app):
        self.app = app

    def create_option_frame(self, title, options):
        """Creates a frame for the options and displays them."""
        option_frame = tk.Frame(self.app.content_frame, bg="#eafce9", bd=2, relief="raised")
        option_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        title_label = tk.Label(option_frame, text=title, font=("Helvetica", 20), bg="#eafce9")
        title_label.pack(pady=10)

        for label, command in options:
            button = tk.Button(option_frame, text=label, command=command, width=20, height=2, font=("Helvetica", 16))
            button.pack(pady=10)

    def show_instructor_management(self):
        """Display instructor management options."""
        self.clear_current_frame()

        # Buttons for instructor operations
        tk.Button(
            self.app.content_frame,
            text="Add Instructor",
            command=self.add_instructor,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="Edit Instructor",
            command=self.edit_instructor,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="Delete Instructor",
            command=self.delete_instructor,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="View Instructors",
            command=self.view_instructors,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

    def add_instructor(self):
        """Adds a new instructor."""
        try:
            name = simpledialog.askstring("Input", "Enter instructor's name:")
            phone = simpledialog.askstring("Input", "Enter instructor's phone:")
            email = simpledialog.askstring("Input", "Enter instructor's email:")

            if not name or not phone or not email:
                messagebox.showwarning("Validation Error", "All fields must be filled!")
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO instructors (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Instructor added successfully!")
        except Exception as e:
            handle_error(e)

    def edit_instructor(self):
        """Edits an existing instructor."""
        try:
            instructor_id = simpledialog.askinteger("Input", "Enter the ID of the instructor to edit:")
            if not instructor_id:
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM instructors WHERE id=?", (instructor_id,))
            instructor = c.fetchone()
            if not instructor:
                messagebox.showwarning("Not Found", "Instructor not found!")
                return

            name = simpledialog.askstring("Edit", f"Enter new name (current: {instructor[1]}):", initialvalue=instructor[1])
            phone = simpledialog.askstring("Edit", f"Enter new phone (current: {instructor[2]}):", initialvalue=instructor[2])
            email = simpledialog.askstring("Edit", f"Enter new email (current: {instructor[3]}):", initialvalue=instructor[3])

            c.execute("UPDATE instructors SET name=?, phone=?, email=? WHERE id=?",
                      (name, phone, email, instructor_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Instructor details updated successfully!")
        except Exception as e:
            handle_error(e)

    def delete_instructor(self):
        """Deletes an instructor."""
        try:
            instructor_id = simpledialog.askinteger("Input", "Enter the ID of the instructor to delete:")
            if not instructor_id:
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("DELETE FROM instructors WHERE id=?", (instructor_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Instructor deleted successfully!")
        except Exception as e:
            handle_error(e)

    def view_instructors(self):
        """Displays a list of instructors."""
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM instructors")
            instructors = c.fetchall()
            conn.close()

            self.clear_current_frame()
            instructor_list_frame = tk.Frame(self.app.content_frame, bg="#f3f3f3")
            instructor_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for instructor in instructors:
                tk.Label(instructor_list_frame, text=f"ID: {instructor[0]}, Name: {instructor[1]}, Email: {instructor[3]}",
                         bg="#0675c2", font=("Arial", 12)).pack(pady=5, anchor="w")
        except Exception as e:
            handle_error(e)

    def clear_current_frame(self):
        """Clears the content frame."""
        for widget in self.app.content_frame.winfo_children():
            widget.destroy()