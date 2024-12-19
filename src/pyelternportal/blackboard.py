""" Black board module """

from dataclasses import dataclass
from datetime import date

from .attachment import Attachment

@dataclass
class BlackBoard():
    """Class representing a black board"""
    sent: date
    subject: str
    body: str
    attachment: Attachment
