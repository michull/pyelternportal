"""Poll module"""

import dataclasses
import datetime

@dataclasses.dataclass
class Poll:
    """Class representing a poll"""
    title: str
    href: str
    attachment: bool
    vote: datetime.datetime
    end: datetime.datetime
    detail: str
