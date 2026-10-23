# Expense Tracker

A simple backend expense-tracking application built with Python, SQLAlchemy ORM, and SQLite. It allows users to organize expenses by category and calculate their total spending.

## Features

- Create and manage expense categories for each user.
- Record expenses with descriptions, amounts, dates, and categories.
- Retrieve expenses belonging to a specific user.
- Calculate total spending.
- Enforce basic data validation and database relationships.
- Use database transactions to maintain data consistency.
- Run automated tests with pytest.

## Tech Stack

- **Python** — application logic
- **SQLAlchemy ORM** — database models and queries
- **SQLite** — data storage
- **pytest** — automated testing

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/EmmanuelDania-Dev/sqlalchemy-expense-tracker.git
cd expense-tracker
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the database tables

```bash
python -c "from app.database import create_tables; create_tables()"
```

### 5. Add sample data

```bash
python seed.py
```

This creates sample users, categories, and expenses in the local SQLite database.

## Running Tests

Run the automated test suite with:

```bash
python -m pytest -v
```

The tests cover expense creation, total spending calculations, validation, user-category ownership, and transaction rollback.

## Project Structure

```text
expense-tracker/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── expenses.py
├── tests/
│   └── test_expenses.py
├── seed.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Demo

This is a demo recording showing the project running successfully:

https://drive.google.com/file/d/1MykplGxqR4JyUszaNV7d16ZQB24yTMIv/view?usp=sharing

## Note

This is a backend project focused on relational database modelling, SQLAlchemy ORM, data validation, and testing. It does not currently include a web interface or API endpoints.

