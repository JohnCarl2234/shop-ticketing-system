# 
from pydantic import BaseModel, field_validator
from database.db_operations import add_client
import logging
import re

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class ValidateClient(BaseModel):

    client_name : str
    contact_number : str
    email : str
    address : str

    @field_validator('client_name')
    @classmethod
    def isthere_client_name(cls, name: str) -> str:
        if not name:
            raise ValueError("Name is required.")
        return name

    @field_validator("contact_number")
    @classmethod
    def validate_mobile_number(cls, mobile_number: str) -> str:
        if not mobile_number:
            raise ValueError("Mobile number is required.")
        else:
            pattern = r"^\+639\d{9}$"
            if not re.fullmatch(pattern, mobile_number):
                raise ValueError("Mobile number is invalid.")
        return mobile_number
            
    @field_validator('email')
    @classmethod
    def validate_email_entry(cls, email:str=None) -> str:
        if email:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.fullmatch(pattern, email):
                raise ValueError("Email field is invalid.")
        return email

    @field_validator("address")
    @classmethod
    def isthere_address(cls, address: str) -> str:
        if not address:
            raise ValueError("Address field is empty")
        return address
    
# create a validate instance
# when creating an instance, use dictionaries then use the unpack **dict notation 

def save_to_db(client: ValidateClient):
    # sends the client information to in the database
    add_client(f"{client.client_name}", f"{client.contact_number}", f"{client.email}", f"{client.address}") 
    logging.info("Client information has been stored successfully.") # logs if the customer_info has been saved

# api template:
# follow the template or use unpacking methods for database processing.

# data_from_ui = {
#     'client_name' : "Jose P. Rizal",
#     'contact_number' :  "+639986761126", 
#     'email' : "arianagrace.mergal@universityofmadrid.edu.sp",
#     'address': "Barangay 68-B, Sagkahan District, Tacloban City"
# }

# save_to_db(ValidateClient(**data_from_ui))