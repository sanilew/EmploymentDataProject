from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
import sqlite3
from faker import Faker
import random

app = Flask(__name__)
api = Api(app)
fake = Faker()

def get_db_connection():
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        department TEXT,
                        salary REAL)''')
    conn.commit()
    conn.close()

class EmployeeList(Resource):
    def get(self):
        conn = get_db_connection()
        employees = conn.execute('SELECT * FROM employees').fetchall()
        conn.close()
        return jsonify([dict(ix) for ix in employees])

    def post(self):
        conn = get_db_connection()
        name = fake.name()
        age = random.randint(20, 65)
        department = random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'])
        salary = round(random.uniform(30000, 120000), 2)
        conn.execute('INSERT INTO employees (name, age, department, salary) VALUES (?, ?, ?, ?)', (name, age, department, salary))
        conn.commit()
        conn.close()
        return {'message': 'Employee created'}, 201

@app.route('/visualize')
def visualize():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    departments = {}
    ages = []
    for emp in employees:
        departments[emp['department']] = departments.get(emp['department'], 0) + 1
        ages.append(emp['age'])
    return render_template('visualize.html', departments=departments, ages=ages)

api.add_resource(EmployeeList, '/employees')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
