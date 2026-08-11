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

# Client and Technician Table
clients = """ CREATE TABLE IF NOT EXISTS Clients (
        cli_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        client TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        email TEXT,
        address TEXT NOT NULL
)
"""
technicians = f""" CREATE TABLE IF NOT EXISTS Agents (
         agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
         agent TEXT,
         assignment TEXT NOT NULL
)
"""
# change tkt_id to client_id
# Ticket table (Parents: clients, technicians)
tickets = f""" CREATE TABLE IF NOT EXISTS Tickets (
        order_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        tkt_ref TEXT GENERATED ALWAYS AS ('SVC' || printf('%03d{date.today().year}', order_id)) STORED UNIQUE,
        order_date DATE,
        tkt_inf TEXT NOT NULL,
        resolved_at DATETIME DEFAULT NULL, 
        status TEXT GENERATED ALWAYS AS (CASE WHEN resolved_at IS NOT NULL AND resolved_at != "None" THEN 'Resolved' ELSE 'Open' END) STORED,
        tkt_id INTEGER,     
        agent_id INT DEFAULT 1,
        FOREIGN KEY (tkt_id) REFERENCES Clients(cli_id) ON DELETE CASCADE,
        FOREIGN KEY (agent_id) REFERENCES Agents(agent_id) ON DELETE SET DEFAULT
)
"""

def run_setup():
    try: 
        cursor(setup_conn()).execute(clients)
        cursor(setup_conn()).execute(tickets)
        cursor(setup_conn()).execute(technicians)
        setup_conn().commit()
    except sqlite3.OperationalError as e:
        print(f"Operational Error (Database): {e}")
    finally: # runs regardless of the state
        setup_conn().close()

if not file.is_file():
    if __name__ == "__main__":
        run_setup()
else:
    print(f"Database: Setup will not execute since the file is found at {file}")