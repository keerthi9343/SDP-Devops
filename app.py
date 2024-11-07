# app.py

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(100), nullable=False)

# Create all tables if they don't exist
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Display Students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

# Add a Student
@app.route('/students', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    major = request.form['major']
    new_student = Student(name=name, age=age, major=major)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('get_students'))

# Edit Student
@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.major = request.form['major']
        db.session.commit()
        return redirect(url_for('get_students'))
    return render_template('edit_student.html', student=student)

# Delete Student
@app.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('get_students'))

if __name__ == '__main__':
    app.run(debug=True)
