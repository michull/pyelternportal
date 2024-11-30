""" Register module """

# pylint: disable=too-many-instance-attributes

from dataclasses import dataclass
from datetime import date

@dataclass
class Register():
    """Class representing a register"""
    subject: str
    short: str
    teacher: str
    lesson: str
    substitution: bool
    empty: bool
    rtype: str
    start: date
    completion: date
    body: str
