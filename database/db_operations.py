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
        if resolved_at == None:
            raise UserWarning("'resolved_at' parameter is empty.")
    except UserWarning as e:
        print(f"Warning in db_operations.add_ticket(): {e}")
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

# Reassigns open ticket to an existing agent before soft deleting
def reassign_ticket(old_agent, new_agent):
    query = "UPDATE Tickets SET agent_id = ? WHERE agent_id = ? AND status = 'Open'"
    return cursor.execute(query, (f"{old_agent}",f"{new_agent}")), connect.commit()

# Gets all the clients list
def get_client(client_id):
    query = """
        SELECT 
        c.cli_id,
        c.client
        c.contact_number,
        c.tkt_ref,
        c.order_id, 
        t.tkt_inf,
        t.status,
        t.order_date,
        a.agent_name,
        FROM Clients c
        JOIN Tickets t ON c.cli_id = t.client_id
        LEFT JOIN Agents a ON t.agents_id = a.agent_id
        WHERE c.cli_id = ?;
    """ 
    cursor.execute(query, ("cli_id"))
    rows = cursor.fetchall()
    # Results will be stored in a clean list for UI
    results = []
    for row in rows:
        results.append({
            "client_id" : row[0],
            "client_name" : row[1],
            "contact_number": row[2], 
            "client_ref" : row[3],
            "ticket_id" : row[4],
            "issue" : row[5],
            "status" : row[6], 
            "date_created" : row[7],
            "agent_assigned" : row[8]
        })
    return results