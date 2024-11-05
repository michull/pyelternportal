"""Student module"""

# pylint: disable=too-many-instance-attributes

import re

from .appointment import Appointment
from .blackboard import BlackBoard
from .lesson import Lesson
from .letter import Letter
from .message import Message
from .poll import Poll
from .register import Register
from .sicknote import SickNote


class Student:
    """Class representing a student"""

    def __init__(self, student_id: str, fullname: str):

        try:
            match = re.search(r"^(\S+)\s+(.*)\s+\((\S+)\)$", fullname)
            firstname = match[1]
            lastname = match[2]
            classname = match[3]
        except TypeError:
            firstname = f"S{student_id}"
            lastname = None
            classname = None

        self.student_id: str = student_id
        self.fullname: str = fullname
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.classname: str = classname

        self.appointments: list[Appointment] = []
        self.blackboards: list[BlackBoard] = []
        self.lessons: list[Lesson] = []
        self.letters: list[Letter] = []
        self.messages: list[Message] = []
        self.polls: list[Poll] = []
        self.registers: list[Register] = []
        self.sicknotes: list[SickNote] = []
