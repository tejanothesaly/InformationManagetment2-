from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'students.db'

# Create a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the students table
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create the table when the application starts
create_table()

# Example CRUD operations for students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return jsonify(dict(student)) if student else jsonify({"message": "Student not found"})


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if name and email:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "Student added successfully"})
    else:
        return jsonify({"message": "Invalid data provided"}), 400  # Bad Request status


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    name = data['name']
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, email=? WHERE id=?", (name, email, student_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated successfully"})


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted successfully"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001)

