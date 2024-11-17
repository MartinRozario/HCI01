import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import handle_error

class StudentManagement:
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

    def show_student_management(self):
        options = [
            ("Add Student", self.add_student),
            ("Edit Student", self.edit_student),
            ("Delete Student", self.delete_student),
            ("View Students", self.view_students),
            ("View Payment Status", self.view_payment_status),
            ("View Lesson Records", self.view_lesson_records),
        ]
        self.create_option_frame("Student Management", options)

    def add_student(self):
        try:
            name = simpledialog.askstring("Input", "Enter student's name:")
            address = simpledialog.askstring("Input", "Enter student's address:")
            phone = simpledialog.askstring("Input", "Enter student's phone:")
            progress = simpledialog.askstring("Input",
                                              "Enter student's progress (e.g., Beginner, Intermediate, Advanced):")
            payment_status = simpledialog.askstring("Input", "Enter payment status (e.g., Paid, Pending):")

            # Validate if any field is empty
            if not name or not address or not phone or not progress or not payment_status:
                messagebox.showwarning("Validation Error", "All fields must be filled in!")
                return  # Don't proceed if any field is empty

            # If all fields are filled, insert into the database
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO students (name, address, phone, progress, payment_status) VALUES (?, ?, ?, ?, ?)",
                      (name, address, phone, progress, payment_status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            handle_error(e)

    def view_students(self):
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM students")
            students = c.fetchall()
            conn.close()

            # Display students in a new window or in the current frame
            self.clear_current_frame()
            student_list_frame = tk.Frame(self.app.content_frame, bg="#eafce9", bd="10", relief="raised")
            student_list_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

            for student in students:
                tk.Label(student_list_frame, text=f"ID: {student[0]}, Name: {student[1]}, Progress: {student[4]}",
                         bg="#eafce9", fg="#0b9cbf").pack(pady=10, anchor="w")
        except Exception as e:
            handle_error(e)

    def edit_student(self):
        try:
            student_id = simpledialog.askinteger("Input", "Enter the ID of the student to edit:")
            if not student_id:
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM students WHERE id=?", (student_id,))
            student = c.fetchone()
            if not student:
                messagebox.showwarning("Not Found", "Student not found!")
                return

            name = simpledialog.askstring("Edit", f"Enter new name (current: {student[1]}):", initialvalue=student[1])
            address = simpledialog.askstring("Edit", f"Enter new address (current: {student[2]}):",
                                             initialvalue=student[2])
            phone = simpledialog.askstring("Edit", f"Enter new phone (current: {student[3]}):", initialvalue=student[3])
            progress = simpledialog.askstring("Edit", f"Enter new progress (current: {student[4]}):",
                                              initialvalue=student[4])
            payment_status = simpledialog.askstring("Edit", f"Enter new payment status (current: {student[5]}):",
                                                    initialvalue=student[5])

            c.execute("UPDATE students SET name=?, address=?, phone=?, progress=?, payment_status=? WHERE id=?",
                      (name, address, phone, progress, payment_status, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student details updated successfully!")
        except Exception as e:
            handle_error(e)

    def delete_student(self):
        try:
            student_id = simpledialog.askinteger("Input", "Enter the ID of the student to delete:")
            if not student_id:
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as e:
            handle_error(e)

    def add_payment(self):
        """Adds a payment record for a student."""
        try:
            # Get the student's ID
            student_id = simpledialog.askinteger("Input", "Enter the student's ID:")
            if not student_id:
                return  # Ensure student_id is provided

            # Ask for payment details
            amount = simpledialog.askfloat("Input", "Enter payment amount:")
            if not amount:
                messagebox.showwarning("Validation Error", "Payment amount must be provided!")
                return

            payment_date = simpledialog.askstring("Input", "Enter payment date (YYYY-MM-DD):")
            if not payment_date:
                messagebox.showwarning("Validation Error", "Payment date must be provided!")
                return

            # Insert payment details into the database
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO payments (student_id, amount, payment_date) VALUES (?, ?, ?)",
                      (student_id, amount, payment_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Payment added successfully!")
        except Exception as e:
            handle_error(e)

    def view_payment_status(self):
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()

            # Query to fetch payment details along with student information
            c.execute('''SELECT payments.id, students.name, payments.amount, payments.payment_date
                         FROM payments
                         INNER JOIN students ON payments.student_id = students.id''')

            payments = c.fetchall()  # Retrieve all payment records
            conn.close()

            self.clear_current_frame()

            if payments:  # Check if any payments are found
                payment_frame = tk.Frame(self.app.content_frame, bg="#eafce9", bd=2, relief="raised")
                payment_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

                # Display each payment record with student name
                for payment in payments:
                    tk.Label(payment_frame,
                             text=f"Payment ID: {payment[0]}, Student: {payment[1]}, Amount: {payment[2]}, Date: {payment[3]}",
                             bg="#eafce9", fg="black").pack(pady=5, anchor="w")
            else:
                # If no records found
                tk.Label(self.app.content_frame, text="No payment records found", font=("Arial", 18, "bold"),
                         fg="red").pack(pady=20)

        except Exception as e:
            handle_error(e)

    def view_lesson_records(self):
        try:
            student_id = simpledialog.askinteger("Input", "Enter the ID of the student to view lessons:")
            if not student_id:
                return  # Ensure student_id is provided

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM lessons WHERE student_id=?", (student_id,))  # Use parameterized queries
            lessons = c.fetchall()
            conn.close()

            if not lessons:
                messagebox.showinfo("No Lessons", "No lessons found for this student.")
                return

            self.clear_current_frame()
            lesson_frame = tk.Frame(self.app.content_frame, bg="#ffffff", bd=2, relief="sunken")
            lesson_frame.grid(row=0, column=0, padx=20, pady=20, sticky="")

            for lesson in lessons:
                tk.Label(lesson_frame,
                         text=f"Lesson ID: {lesson[0]}, Type: {lesson[3]}, Date: {lesson[4]}, Status: {lesson[5]}",
                         bg="#ffffff", fg="black").grid(pady=5, sticky="w")
        except Exception as e:
            handle_error(e)

    def show_student_management(self):
        """Display student management options, including payment and lesson records."""
        # Clear the current frame
        for widget in self.app.content_frame.winfo_children():  # Access content_frame via self.app
            widget.destroy()

        # Add buttons for student management options (using pack only)
        tk.Button(
            self.app.content_frame,  # Access content_frame via self.app
            text="Add Student",
            command=self.add_student,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,  # Access content_frame via self.app
            text="Edit Student",
            command=self.edit_student,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,  # Access content_frame via self.app
            text="Delete Student",
            command=self.delete_student,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,  # Access content_frame via self.app
            text="View Students",
            command=self.view_students,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        # New Add Payment Button
        tk.Button(
            self.app.content_frame,
            text="Add Payment",
            command=self.add_payment,  # New method to add payment
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Add buttons for the new options: View Payment Status and View Lesson Records
        tk.Button(
            self.app.content_frame,
            text="View Payment Status",
            command=self.view_payment_status,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="View Lesson Records",
            command=self.view_lesson_records,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)



    def clear_current_frame(self):
        """Clears the current frame before switching views."""
        for widget in self.app.content_frame.winfo_children():
            widget.destroy()