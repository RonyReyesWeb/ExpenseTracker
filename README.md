# Overview

As a software engineer, I wanted to learn how to build software that stores
and manages data in a relational database using SQL. This project helped me
practice designing tables, writing SQL statements, and running them from my
own code.

The Expense Tracker is a command-line program written in Python that keeps a
record of daily expenses in a SQLite database. From a menu, the user can add
a new expense, view all saved expenses with a running total, edit an
expense's description and amount, and delete an expense. To start the
program, run `python expense_tracker.py` in a terminal. The database file
(`expenses.db`) is created automatically the first time the program runs.

My purpose for writing this software was to learn how a program builds SQL
commands, sends them to a database, receives the results, and uses those
results to show useful information to the user.

[Software Demo Video](https://www.youtube.com/watch?v=lA5UtVAl-TI&feature=youtu.be)

# Relational Database

I used SQLite, a lightweight relational database that is stored in a single
file and comes built into Python.

The database has two related tables:

- **categories** – `id` (primary key) and `name` (Food, Rent, Transport,
  Utilities, Entertainment, Other)
- **expenses** – `id` (primary key), `date`, `description`, `amount`, and
  `category_id`, a foreign key that references `categories.id`

The program uses a `JOIN` between the two tables to display each expense
with its category name.

# Development Environment

- Visual Studio Code
- Git and GitHub
- DB Browser for SQLite (for testing queries)
- Python 3 with the built-in `sqlite3` library

# Useful Websites

- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite documentation](https://www.sqlite.org/docs.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)

# Future Work

- Show total and average spending per category using `SUM` and `AVG`
- Filter expenses by a date range (for example, one month)
- Let the user add their own categories
