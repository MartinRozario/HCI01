import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import handle_error

class LessonManagement:
    def __init__(self, app):
        self.app = app

    def show_lesson_management(self):
        """Displays lesson management options."""
        self.clear_current_frame()

        # Buttons for lesson operations
        tk.Button(
            self.app.content_frame,
            text="Schedule Lesson",
            command=self.schedule_lesson,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="Update Lesson Status",
            command=self.update_lesson_status,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="View Lessons",
            command=self.view_lessons,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

    def schedule_lesson(self):
        """Schedules a new lesson."""
        try:
            student_id = simpledialog.askinteger("Input", "Enter the student's ID:")
            instructor_id = simpledialog.askinteger("Input", "Enter the instructor's ID:")
            lesson_type = simpledialog.askstring("Input", "Enter lesson type (e.g., Driving, Theory):")
            lesson_date = simpledialog.askstring("Input", "Enter lesson date (YYYY-MM-DD):")
            status = simpledialog.askstring("Input", "Enter lesson status (e.g., Scheduled, Completed):")

            if not student_id or not instructor_id or not lesson_type or not lesson_date or not status:
                messagebox.showwarning("Validation Error", "All fields must be filled!")
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO lessons (student_id, instructor_id, lesson_type, date, status) VALUES (?, ?, ?, ?, ?)",
                      (student_id, instructor_id, lesson_type, lesson_date, status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Lesson scheduled successfully!")
        except Exception as e:
            handle_error(e)

    def update_lesson_status(self):
        """Updates the status of an existing lesson."""
        try:
            lesson_id = simpledialog.askinteger("Input", "Enter the lesson ID to update:")
            if not lesson_id:
                return

            new_status = simpledialog.askstring("Input", "Enter the new lesson status:")
            if not new_status:
                messagebox.showwarning("Validation Error", "Status cannot be empty!")
                return

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("UPDATE lessons SET status=? WHERE id=?", (new_status, lesson_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Lesson status updated successfully!")
        except Exception as e:
            handle_error(e)

    def view_lessons(self):
        """Displays all scheduled lessons."""
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM lessons")
            lessons = c.fetchall()
            conn.close()

            self.clear_current_frame()
            lesson_list_frame = tk.Frame(self.app.content_frame, bg="#fdfdfd")
            lesson_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for lesson in lessons:
                tk.Label(lesson_list_frame,
                         text=f"ID: {lesson[0]}, Type: {lesson[3]}, Date: {lesson[4]}, Status: {lesson[5]}",
                         bg="#0675c2", font=("Arial", 12)).pack(pady=5, anchor="w")
        except Exception as e:
            handle_error(e)

    def clear_current_frame(self):
        """Clears the content frame."""
        for widget in self.app.content_frame.winfo_children():
            widget.destroy()