import sqlite3
from pathlib import Path
from datetime import date

# inserting data in the client database

app_data = Path("./data/app_data.db")


def _get_connection():
    if not app_data.is_file():
        raise FileNotFoundError("db_operations.py: File not found in the supposed directory.")

    connection = sqlite3.connect(app_data)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

# Query functions
def add_client(name: str, contact_number: str, mail: str, address: str):
    query = """INSERT INTO Clients (client, contact_number, email, address) 
    VALUES (?, ?, ?, ?)"""
    try:
        with _get_connection() as connection:
            connection.execute(query, (f"{name}", f"{contact_number}", f"{mail}", f"{address}"))
    except (sqlite3.OperationalError, FileNotFoundError) as e:
        return f"sqlite3 client query error: {e}"

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
    with _get_connection() as connection:
        return connection.execute(query, (f"{client_id}", f"{tkt_info}", f"{day}", f"{resolved_at}", f"{agent_id}"))

# Employing new agent 
def add_agent(name, assignment):
    query = "INSERT INTO Agents (agent_name, assignment) VALUES (?, ?)"
    with _get_connection() as connection:
        return connection.execute(query, (f"{name}", f"{assignment}"))

# Deactivates agents that left the organization via soft delete so that 
# existing open tickets and old tickets could be reassigned/determined 
# the assigned personnel. # 0 -> Deactivated, 1 -> Active
def deactivating_agent(agent_id, state):
    query = "UPDATE Agents SET is_active = ? WHERE agent_id = ?"
    with _get_connection() as connection:
        return connection.execute(query, (f"{state}", f"{agent_id}"))

# Deleting user data
def delete_client(client_name):
    query = "DELETE FROM Clients WHERE client = ?"
    with _get_connection() as connection:
        return connection.execute(query, (f"{client_name}",))

# Reassigns open ticket to an existing agent before soft deleting
def reassign_ticket(old_agent, new_agent):
    query = "UPDATE Tickets SET agent_id = ? WHERE agent_id = ? AND status = 'Open'"
    with _get_connection() as connection:
        return connection.execute(query, (f"{old_agent}",f"{new_agent}"))

# Fetch function for UI:
def query_fetch_transaction(client_name):
    query = """
        SELECT 
                c.cli_id,
                c.client,
                c.contact_number,
                c.tkt_ref,
                t.order_id,
                t.tkt_inf,
                t.status,
                t.order_date,
                a.agent_name
            FROM Clients c
            JOIN Tickets t ON c.cli_id = t.client_id
            LEFT JOIN Agents a ON t.agent_id = a.agent_id
            WHERE c.client = ?;
    """ 
    with _get_connection() as connection:
        cursor = connection.execute(query, (f"{client_name}",))
        # fetch data from the database for UI
        rows = cursor.fetchall()
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

def check_client(cli_id: int) -> bool:
    with _get_connection() as connection:
        query = "SELECT EXISTS(SELECT 1 From Clients WHERE cli_id = ?)"
        cursor = connection.cursor()
        cursor.execute(query, (f"{str(cli_id)}",))
        result = cursor.fetchone()[0]
        return bool(result) 

def agent_state(agent_id: int) -> bool:
    with _get_connection() as connection:
        query = "SELECT is_active FROM Agents WHERE agent_id = ?"
        cursor = connection.cursor()
        cursor.execute(query, (f"{str(agent_id)}",))
        row = cursor.fetchone()
        if row[0] == 1:
            return True
        else: 
            False