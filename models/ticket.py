from pydantic import BaseModel, field_validator, Field
from database.db_operations import check_client, agent_state
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class ValidateTicket(BaseModel):
    issue_text:str=Field(max_length=150)
    client_reference_id : int
    agent_assigned : Optional[str]
    date : Optional[str]
    status: str

    @field_validator("issue_text")
    @classmethod
    def validate_issue_field(cls, issue: str):
        if not issue:
            raise ValueError("Issue field is empty.")
        return issue

    @field_validator("client_reference")
    @classmethod
    def does_client_exist(cls, referential_id: int):
        if not check_client(referential_id):
            raise ValueError("Client reference id for this ticket is not found in the database.")
        return referential_id

    @field_validator("agent_assigned")
    @classmethod
    def is_agent_valid(cls, agent_status: int):
        if agent_status:
            if not agent_state(agent_status):
                raise ValueError("Agent is inactive")

# def is_issue(present_issue: ValidateTicket):
#     return f"Present issue: {present_issue.issue_text}"

# data_1 = {"issue_text": "Waray salapi"}

# print(is_issue(ValidateTicket(**data_1)))