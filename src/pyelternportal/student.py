"""Student module"""

# pylint: disable=too-many-instance-attributes

import re
from typing import Any

from .appointment import Appointment
from .blackboard import BlackBoard
from .lesson import Lesson
from .letter import Letter
from .message import Message
from .poll import Poll
from .register import Register
from .sicknote import SickNote
from .substitution import Substitution


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
        self.substitutions: list[Substitution] = []

    def get_list(self, key: str) -> list[Any] | None:
        """Get list of elements"""
        match key:
            case "appointments":
                result: list[Appointment] = self.appointments
            case "blackboards":
                result: list[BlackBoard] = self.blackboards
            case "lessons":
                result: list[Lesson] = self.lessons
            case "letters":
                result: list[Letter] = self.letters
            case "messages":
                result: list[Message] = self.messages
            case "polls":
                result: list[Poll] = self.polls
            case "registers":
                result: list[Register] = self.registers
            case "sicknotes":
                result: list[SickNote] = self.sicknotes
            case "substitutions":
                result: list[Substitution] = self.substitutions
            case _:
                result = None
        return result

    def get_list_len(self, key: str) -> int | None:
        """Get number of elements"""
        match key:
            case "appointments":
                result: int = len(self.appointments)
            case "blackboards":
                result: int = len(self.blackboards)
            case "lessons":
                result: int = len(self.lessons)
            case "letters":
                result: int = len(self.letters)
            case "messages":
                result: int = len(self.messages)
            case "polls":
                result: int = len(self.polls)
            case "registers":
                result: int = len(self.registers)
            case "sicknotes":
                result: int = len(self.sicknotes)
            case "substitutions":
                result: int = len(self.substitutions)
            case _:
                result = None
        return result
