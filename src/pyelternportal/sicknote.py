""" Sick note module """

from dataclasses import dataclass
from datetime import date

@dataclass
class SickNote():
    """Class representing a sick note"""
    start: date
    end: date
    comment: str
