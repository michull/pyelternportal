"""Message module"""

import dataclasses
import datetime

@dataclasses.dataclass
class Message:
    """Class representing a message"""
    sender: str
    sent: datetime.datetime
    new: bool
    subject: str
    body: str
