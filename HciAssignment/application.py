import tkinter as tk
from student_management import StudentManagement
from instructor_management import InstructorManagement
from lesson_management import LessonManagement
from reporting import Reporting


class Application:
    def __init__(self, root):
            self.root = root
            self.root.title("Pass IT Driving School Management System")
            self.root.state("zoomed")
            self.root.config(bg="#e0eff2")

            # Initialize Student Management
            self.student_management = StudentManagement(self) #newly added
            self.instructor_management = InstructorManagement(self)
            self.lesson_management = LessonManagement(self)
            self.reporting = Reporting(self)

            # Main frame
            self.main_frame = tk.Frame(self.root, bg="#e0eff2")
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Content frame
            self.content_frame = tk.Frame(self.main_frame, bg="#ffd966", relief=tk.RAISED, bd=2)
            self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.create_widgets()

    def create_widgets(self):
        # Button frame
        button_frame = tk.Frame(self.main_frame, bg="#b6d7a8")
        button_frame.pack(fill=tk.X, pady=10)

        # Buttons
        student_button = tk.Button(
            button_frame,
            text="Student Management",
            command=self.student_management.show_student_management,  # Connect to StudentManagement class #Changed
            bg="#b6d7a8",
            fg="black",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=5,
        )
        instructor_button = tk.Button(
            button_frame,
            text="Instructor Management",
            command=self.instructor_management.show_instructor_management,  # Call InstructorManagement's method
            bg="#b6d7a8",
            fg="black",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=5,
        )
        lesson_button = tk.Button(
            button_frame,
            text="Lesson Management",
            command=self.lesson_management.show_lesson_management,
            bg="#b6d7a8",
            fg="black",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=5,
        )
        report_button = tk.Button(
            button_frame,
            text="Reporting",
            command=self.reporting.show_reporting,
            bg="#b6d7a8",
            fg="black",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=5,
        )

        # Layout buttons in button_frame
        student_button.pack(side=tk.LEFT, padx=5, pady=5)
        instructor_button.pack(side=tk.LEFT, padx=5, pady=5)
        lesson_button.pack(side=tk.LEFT, padx=5, pady=5)
        report_button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_student_management(self):
        """Displays the Student Management screen."""
        self.clear_content()
        tk.Label(self.content_frame, text="Student Management", font=("Arial", 18, "bold")).pack(pady=20)

    def show_instructor_management(self):
        """Displays the Instructor Management screen."""
        self.clear_content()
        tk.Label(self.content_frame, text="Instructor Management", font=("Arial", 18, "bold")).pack(pady=20)

    def show_lesson_management(self):
        """Displays the Lesson Management screen."""
        self.clear_content()
        tk.Label(self.content_frame, text="Lesson Management", font=("Arial", 18, "bold")).pack(pady=20)

    def show_reporting(self):
        """Displays the Reporting screen."""
        self.clear_content()
        tk.Label(self.content_frame, text="Reporting", font=("Arial", 18, "bold")).pack(pady=20)


    def clear_content(self):
        """Clears the content frame before switching views."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()