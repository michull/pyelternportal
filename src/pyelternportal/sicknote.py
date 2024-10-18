""" Sick note module """

import dataclasses
import datetime

@dataclasses.dataclass
class SickNote():
    """Class representing a sick note"""
    start: datetime.date
    end: datetime.date
    comment: str
