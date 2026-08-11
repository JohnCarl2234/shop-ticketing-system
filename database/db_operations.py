import sqlite3
from pathlib import Path

# inserting data in the client database

# Updating data of a specific entry/item
# c.execute("UPDATE employees SET name = '', age = '' WHERE id = '' ")
# Updating an entire column
# c.execute("UPDATE employees SET state = ''")

# deleting a specific item by its table and column value
# c.execute("DELETE FROM employees WHERE first_name = 'Rishelvin'")

# deleting a whole table
# c.execute("DROP TABLE IF EXISTS employees")


app_data = Path("./data/app_data.db")
# Checks if the directory is created.

try:
    if app_data.is_file():
        connect = sqlite3.connect(app_data)
        print("db_operations.py: Linked successfully.")
    else:
        raise NotADirectoryError("db_operations.py: File not found in the supposed directory.")
except NotADirectoryError as e:
    print(e)
