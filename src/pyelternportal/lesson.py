""" Lesson module """

from dataclasses import dataclass

@dataclass
class Lesson():
    """Class representing a lesson"""
    weekday: int
    number: str
    subject: str
    room: str
