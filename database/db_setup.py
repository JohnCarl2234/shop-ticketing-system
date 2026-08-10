import sqlite3
from datetime import date
from pathlib import Path

file = Path('./data/app_data.db')

def setup_conn():
    try:
        connection = sqlite3.connect("./data/app_data.db")
        connection.execute("PRAGMA foreign_keys = ON;")
    except sqlite3.OperationalError as e:
        print(f"Operational Error: {e}")
        connection.close()
    return connection

def cursor(connection):
    c = connection.cursor()
    return c

# Setup database interfaces for client, technicians, administrator

tickets = f""" CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        main_id TEXT GENERATED ALWAYS AS ('SVC' || printf('%03d{date.today().year}', id)) STORED UNIQUE,
        ticket_info TEXT NOT NULL,
        client_id INTEGER, 
        FOREIGN KEY (client_id) REFERENCES clients (cli_no)
)
"""

clients = """ CREATE TABLE IF NOT EXISTS clients (
        cli_no INTEGER PRIMARY KEY AUTOINCREMENT,
        cli_name TEXT NOT NULL
)
"""

def run_setup():
    try:
        cursor(setup_conn()).execute(clients)
        cursor(setup_conn()).execute(tickets)
        setup_conn().commit()
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        setup_conn().close()

if not file.is_file():
    if __name__ == "__main__":
        run_setup()
else:
    print(f"Setup will not execute since the file is found at {file}")