import sqlite3
from pathlib import Path
from datetime import date

# inserting data in the client database

app_data = Path("./data/app_data.db")
# Checks if the directory is created.

try:
    if app_data.is_file():
        connect = sqlite3.connect(app_data)
        connect.execute("PRAGMA foreign_keys = ON;")
        print("db_operations.py: Linked successfully.")
    else:
        raise NotADirectoryError("db_operations.py: File not found in the supposed directory.")
except NotADirectoryError as e:
    print(e)

cursor = connect.cursor()

# Query functions
def add_client(name: str, contact_number: str, mail: str, address: str):
    query = """INSERT INTO Clients (client, contact_number, email, address) 
    VALUES (?, ?, ?, ?)"""
    return cursor.execute(query, (f"{name}", f"{contact_number}", f"{mail}", f"{address}")), connect.commit()

# Adding a ticket entry
def add_ticket(client_id: str, tkt_info: str, agent_id: str, resolved_at=None):
    query = """INSERT INTO Tickets (client_id, tkt_inf, order_date, resolved_at, agent_id) 
    VALUES (?, ?, ?, ?, ?)"""
    day = date.today()
    try:
        if resolved_at == "None":
            raise Warning("'resolved_at' variable is empty.")
    except Warning as e:
        print(f"db_operations: {e}")
    return cursor.execute(query, (f"{client_id}", f"{tkt_info}", f"{day}", f"{resolved_at}", f"{agent_id}")), connect.commit()

# Employing new agent 
def add_agent(name, assignment):
    query = "INSERT INTO Agents (agent_name, assignment) VALUES (?, ?)"
    return cursor.execute(query, (f"{name}", f"{assignment}")), connect.commit()

# Deactivates agents that left the organization via soft delete so that 
# existing open tickets and old tickets could be reassigned/determined 
# the assigned personnel. # 0 -> Deactivated, 1 -> Active
def deactivating_agent(agent_id, state):
    query = "UPDATE Agents SET is_active = ? WHERE agent_id = ?"
    return cursor.execute(query, (f"{state}", f"{agent_id}")), connect.commit()

# Deleting user data
def delete_client(entry):
    query = f"DELETE FROM Clients WHERE client = '{entry}'"
    return cursor.execute(query), connect.commit()

# Reassigns open ticket to an existing agent before 
def reassign_ticket(old_agent, new_agent):
    query = "UPDATE Tickets SET agent_id = ? WHERE agent_id = ? AND status = 'Open'"
    return cursor.execute(query, (f"{old_agent}",f"{new_agent}")), connect.commit()