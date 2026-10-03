""" Substitution module """

from dataclasses import dataclass
from datetime import date


@dataclass
class Substitution:
    """Class representing a substitution"""
    date: date
    lesson: str
    original_teacher: str
    substitute_teacher: str
    room: str
    info: str