""" Letter module """

# pylint: disable=too-many-instance-attributes

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Letter():
    """Class representing a letter"""
    letter_id: str
    number: str
    sent: datetime
    new: bool
    attachment: bool
    subject: str
    distribution: str
    body: str
