"""Message module"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    """Class representing a message"""
    sender: str
    sent: datetime
    new: bool
    subject: str
    body: str
