import sqlite3
from utils import handle_error

def create_db():
    try:
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()

        # Create students table
        c.execute('''CREATE TABLE IF NOT EXISTS students (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT,
                     address CHAR,
                     phone INT,
                     progress TEXT,
                     payment_status TEXT)''')

        # Create instructors table
        c.execute('''CREATE TABLE IF NOT EXISTS instructors (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT,
                     phone INT,
                     email CHAR)''')

        # Create lessons table
        c.execute('''CREATE TABLE IF NOT EXISTS lessons (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     student_id INTEGER,
                     instructor_id INTEGER,
                     lesson_type TEXT,
                     date TEXT,
                     status TEXT,
                     FOREIGN KEY(student_id) REFERENCES students(id),
                     FOREIGN KEY(instructor_id) REFERENCES instructors(id))''')

        # Create payments table
        c.execute('''CREATE TABLE IF NOT EXISTS payments (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     student_id INTEGER,
                     amount REAL,
                     payment_date TEXT,
                     FOREIGN KEY(student_id) REFERENCES students(id))''')

        conn.commit()
        conn.close()
    except Exception as e:
        handle_error(e)