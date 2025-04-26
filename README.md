# Employee Data Generation & Visualization Project

## Features
- REST API to get and create employee data
- Fake data generation using Faker
- Data stored in SQLite
- Visualization of employee data (department distribution, age distribution) using Chart.js

## Setup
```bash
pip install -r requirements.txt
python app.py
```
Then visit http://127.0.0.1:5000/visualize to see the charts.

## API Endpoints
- `GET /employees` - List all employees
- `POST /employees` - Generate a new employee
