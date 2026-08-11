import sqlite3
from pathlib import Path
from datetime import date

# inserting data in the client database

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

cursor = connect.cursor()
day = date.today()

def add_client(name: str, contact_number: str, mail: str, address: str):
    query = """INSERT INTO Clients (client, contact_number, email, address) 
    VALUES (?, ?, ?, ?)"""
    return cursor.execute(query, (f"{name}", f"{contact_number}", f"{mail}", f"{address}")), connect.commit()

def add_ticket(client_id: str, tkt_info: str, date: str, agent_id: str, resolved_at=None):
    query = """INSERT INTO Tickets (tkt_id, tkt_inf, order_date, resolved_at, agent_id) 
    VALUES (?, ?, ?, ?, ?)"""
    try:
        if resolved_at == "None":
            raise Warning("'resolved_at' variable is empty.")
    except Warning as e:
        print(f"db_operations: {e}")
    return cursor.execute(query, (f"{client_id}", f"{tkt_info}", f"{date}", f"{resolved_at}", f"{agent_id}")), connect.commit()

def add_agent(name, assignment):
    query = """INSERT INTO Agents (agent, assignment) 
        VALUES (?, ?)"""
    return cursor.execute(query, (f"{name}", f"{assignment}")), connect.commit()
