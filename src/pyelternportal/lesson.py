""" Lesson module """

import dataclasses

@dataclasses.dataclass
class Lesson():
    """Class representing a lesson"""
    weekday: int
    number: str
    subject: str
    room: str
