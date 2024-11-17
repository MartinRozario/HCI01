import sqlite3
import tkinter as tk
from tkinter import messagebox
from utils import handle_error

class Reporting:
    def __init__(self, app):
        self.app = app

    def show_reporting(self):
        """Displays reporting options."""
        self.clear_current_frame()

        # Buttons for generating reports
        tk.Button(
            self.app.content_frame,
            text="Student Report",
            command=self.student_report,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="Instructor Report",
            command=self.instructor_report,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

        tk.Button(
            self.app.content_frame,
            text="Lesson Report",
            command=self.lesson_report,
            width=20,
            height=2,
            font=("Helvetica", 16)
        ).pack(pady=10)

    def student_report(self):
        """Generates a report for all students."""
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("""
                SELECT s.id, s.name, s.phone, COUNT(l.id) as lessons_count
                FROM students s
                LEFT JOIN lessons l ON s.id = l.student_id
                GROUP BY s.id
                ORDER BY lessons_count DESC
            """)
            students = c.fetchall()
            conn.close()

            self.display_report("Student Report", students, ["ID", "Name", "Phone", "Lessons Taken"])
        except Exception as e:
            handle_error(e)

    def instructor_report(self):
        """Generates a report for all instructors."""
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("""
                SELECT i.id, i.name, i.email, COUNT(l.id) as lessons_given
                FROM instructors i
                LEFT JOIN lessons l ON i.id = l.instructor_id
                GROUP BY i.id
                ORDER BY lessons_given DESC
            """)
            instructors = c.fetchall()
            conn.close()

            self.display_report("Instructor Report", instructors, ["ID", "Name", "Email", "Lessons Given"])
        except Exception as e:
            handle_error(e)

    def lesson_report(self):
        """Generates a report for all lessons."""
        try:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("""
                SELECT l.id, s.name as student_name, i.name as instructor_name, l.lesson_type, l.date, l.status
                FROM lessons l
                JOIN students s ON l.student_id = s.id
                JOIN instructors i ON l.instructor_id = i.id
                ORDER BY l.date DESC
            """)
            lessons = c.fetchall()
            conn.close()

            self.display_report(
                "Lesson Report",
                lessons,
                ["ID", "Student", "Instructor", "Type", "Date", "Status"]
            )
        except Exception as e:
            handle_error(e)

    def display_report(self, title, data, headers):
        """Displays a formatted report."""
        self.clear_current_frame()

        tk.Label(self.app.content_frame, text=title, font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        report_frame = tk.Frame(self.app.content_frame, bg="#ffffff")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Headers
        header_row = tk.Frame(report_frame, bg="#cccccc")
        header_row.pack(fill=tk.X, pady=2)
        for header in headers:
            tk.Label(header_row, text=header, font=("Helvetica", 12, "bold"), bg="#cccccc", anchor="w", width=15).pack(side=tk.LEFT, padx=2)

        # Data rows
        for row in data:
            data_row = tk.Frame(report_frame, bg="#f9f9f9")
            data_row.pack(fill=tk.X, pady=1)
            for cell in row:
                tk.Label(data_row, text=cell, font=("Helvetica", 10), bg="#0675c2", anchor="w", width=15).pack(side=tk.LEFT, padx=2)

    def clear_current_frame(self):
        """Clears the content frame."""
        for widget in self.app.content_frame.winfo_children():
            widget.destroy()