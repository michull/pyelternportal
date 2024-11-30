"""Poll module"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Poll:
    """Class representing a poll"""
    title: str
    href: str
    attachment: bool
    vote: datetime
    end: datetime
    detail: str
