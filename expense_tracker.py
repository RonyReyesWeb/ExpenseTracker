"""Expense Tracker

The program demonstrates the knowledge I adquired related to relational database from Python:
  * creating tables (expenses and categories)
  * inserting, updating, deleting and querying rows
  * joining two related tables to show each expense with its category name
"""
import sqlite3

DB_FILE = "expenses.db"

# Categories added the first time the database is created
DEFAULT_CATEGORIES = ["Food", "Rent", "Transport", "Utilities", "Entertainment", "Other"]


def connect(db_file=DB_FILE):
    """Open a connection to the database and make sure foreign keys are enforced."""
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables(conn):
    """Create the categories and expenses tables if they don't exist yet."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            description TEXT NOT NULL,
            amount      REAL NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    # Fill the categories table only if it is empty
    count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if count == 0:
        conn.executemany("INSERT INTO categories (name) VALUES (?)",
                         [(name,) for name in DEFAULT_CATEGORIES])
    conn.commit()


def get_categories(conn):
    """Return a list of (id, name) tuples for every category."""
    return conn.execute("SELECT id, name FROM categories ORDER BY id").fetchall()


def add_expense(conn, date, description, amount, category_id):
    """INSERT a new expense and return its new id."""
    cursor = conn.execute(
        "INSERT INTO expenses (date, description, amount, category_id) VALUES (?, ?, ?, ?)",
        (date, description, amount, category_id),
    )
    conn.commit()
    return cursor.lastrowid


def get_expenses(conn):
    """Query all expenses, using a JOIN to get each expense's category name."""
    return conn.execute("""
        SELECT e.id, e.date, e.description, e.amount, c.name
        FROM expenses AS e
        JOIN categories AS c ON e.category_id = c.id
        ORDER BY e.date, e.id
    """).fetchall()


def update_expense(conn, expense_id, description, amount):
    """UPDATE the description and amount of one expense. Returns True if a row changed."""
    cursor = conn.execute(
        "UPDATE expenses SET description = ?, amount = ? WHERE id = ?",
        (description, amount, expense_id),
    )
    conn.commit()
    return cursor.rowcount > 0


def delete_expense(conn, expense_id):
    """DELETE one expense by id. Returns True if a row was removed."""
    cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return cursor.rowcount > 0


def print_expenses(rows):
    """Display query results as a simple table, with the total at the bottom."""
    if not rows:
        print("\nNo expenses saved yet.")
        return
    print(f"\n{'ID':<4}{'Date':<12}{'Description':<28}{'Amount':>10}  Category")
    print("-" * 66)
    total = 0
    for expense_id, date, description, amount, category in rows:
        print(f"{expense_id:<4}{date:<12}{description[:26]:<28}{amount:>10.2f}  {category}")
        total += amount
    print("-" * 66)
    print(f"{'Total':<44}{total:>10.2f}")


def ask_amount(prompt):
    """Keep asking until the user types a valid positive number."""
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return amount
            print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a number, like 12.50")


def ask_int(prompt):
    """Keep asking until the user types a whole number."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def menu_add(conn):
    """Ask the user for an expense's details and save it."""
    date = input("Date (YYYY-MM-DD): ").strip()
    description = input("Description: ").strip()
    amount = ask_amount("Amount: ")
    categories = get_categories(conn)
    print("Categories: " + ", ".join(f"{cid}={name}" for cid, name in categories))
    valid_ids = [cid for cid, _ in categories]
    category_id = ask_int("Category number: ")
    while category_id not in valid_ids:
        category_id = ask_int("Not a valid category. Category number: ")
    new_id = add_expense(conn, date, description, amount, category_id)
    print(f"Expense saved with ID {new_id}.")


def menu_edit(conn):
    """Ask which expense to change and save the new values."""
    print_expenses(get_expenses(conn))
    expense_id = ask_int("ID of the expense to edit: ")
    description = input("New description: ").strip()
    amount = ask_amount("New amount: ")
    if update_expense(conn, expense_id, description, amount):
        print("Expense updated.")
    else:
        print("No expense with that ID.")


def menu_delete(conn):
    """Ask which expense to remove and delete it."""
    print_expenses(get_expenses(conn))
    expense_id = ask_int("ID of the expense to delete: ")
    if delete_expense(conn, expense_id):
        print("Expense deleted.")
    else:
        print("No expense with that ID.")


def main():
    """Show the menu in a loop until the user chooses to exit."""
    conn = connect()
    create_tables(conn)
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Edit an expense")
        print("4. Delete an expense")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            menu_add(conn)
        elif choice == "2":
            print_expenses(get_expenses(conn))
        elif choice == "3":
            menu_edit(conn)
        elif choice == "4":
            menu_delete(conn)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose 1-5.")
    conn.close()


if __name__ == "__main__":
    main()
