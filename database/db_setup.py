import sqlite3
from datetime import date
from pathlib import Path

folder_path = Path("./data")
file = Path(f'./{folder_path.mkdir(parents=True, exist_ok=True)}/app_data.db')

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

# Parent table
clients = """ CREATE TABLE IF NOT EXISTS clients (
        cli_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        contact TEXT NOT NULL
)
"""

# Child table
tickets = f""" CREATE TABLE IF NOT EXISTS tickets (
        order_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT GENERATED ALWAYS AS ('SVC' || printf('%03d{date.today().year}', order_id)) STORED UNIQUE,
        order_date DATE,
        ticket_info TEXT NOT NULL,
        ticket_id INTEGER, 
        FOREIGN KEY (ticket_id) REFERENCES clients(cli_id) ON DELETE CASCADE,
        agent_id INTEGER DEFAULT 1,
        FOREIGN KEY (agent_id) REFERENCES agents(tech_id) ON DELETE SET DEFAULT
)
"""

technicians = f""" CREATE TABLE IF NOT EXISTS agents (
        tech_id INTEGER UNIQUE PRIMARY KEY,
        technician TEXT,
        assignment VARCHAR(3)
)
"""

def run_setup():
    try:
        cursor(setup_conn()).execute(clients)
        cursor(setup_conn()).execute(tickets)
        cursor(setup_conn()).execute(technicians)
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