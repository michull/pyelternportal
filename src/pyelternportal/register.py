""" Register module """

# pylint: disable=too-many-instance-attributes

import dataclasses
import datetime

@dataclasses.dataclass
class Register():
    """Class representing a register"""
    subject: str
    short: str
    teacher: str
    lesson: str
    substitution: bool
    empty: bool
    rtype: str
    start: datetime.date
    completion: datetime.date
    body: str
