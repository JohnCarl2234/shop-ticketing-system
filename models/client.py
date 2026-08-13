from database.db_operations import add_client, delete_client # imports database operations

class CreateClient:
    # Contructor
    def __init__(self, client_name, contact_number, email, address):
        self._client_name = client_name
        self._contact_number = contact_number
        self._email = email 
        self._address = address
    # Methods
    def store(self):
        add_client(self._client_name, self._contact_number, self._email, self._address)