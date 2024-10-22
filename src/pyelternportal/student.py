"""Student module"""

# pylint: disable=too-many-instance-attributes

import re

from .appointment import Appointment
from .lesson import Lesson
from .letter import Letter
from .poll import Poll
from .register import Register
from .sicknote import SickNote

class Student():
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

        self.appointments: list = []
        self.lessons: list = []
        self.letters: list = []
        self.polls: list = []
        self.registers: list = []
        self.sicknotes: list = []

    def get_id(self) -> str:
        """Get student id"""
        return self.student_id

    def get_fullname(self) -> str:
        """Get full name"""
        return self.fullname

    def get_firstname(self) -> str:
        """Get first name"""
        return self.firstname

    def get_count(self) -> int:
        """Get count of all sequences"""
        return (
            len(self.appointments)
            + len(self.lessons)
            + len(self.letters)
            + len(self.polls)
            + len(self.registers)
            + len(self.sicknotes)
        )

    def set_appointments(self, appointments: list[Appointment]) -> None:
        """set list of appointments"""
        self.appointments = appointments

    def get_appointments(self) -> list[Appointment]:
        """get list of appointments"""
        return self.appointments

    def set_lessons(self, lessons: list[Lesson]) -> None:
        """set list of lessons"""
        self.lessons = lessons

    def get_lessons(self) -> list[Lesson]:
        """get list of lessons"""
        return self.lessons

    def set_letters(self, letters: list[Letter]) -> None:
        """set list of letters"""
        self.letters = letters

    def get_letters(self) -> list[Letter]:
        """get list of letters"""
        return self.letters

    def set_polls(self, polls: list[Poll]) -> None:
        """set list of polls"""
        self.polls = polls

    def get_polls(self) -> list[Poll]:
        """get list of polls"""
        return self.polls

    def set_registers(self, registers: list[Register]) -> None:
        """set list of registers"""
        self.registers = registers

    def get_registers(self) -> list[Register]:
        """get list of registers"""
        return self.registers

    def set_sicknotes(self, sicknotes: list[SickNote]) -> None:
        """set list of sicknotes"""
        self.sicknotes = sicknotes

    def get_sicknotes(self) -> list[SickNote]:
        """get list of sicknotes"""
        return self.sicknotes
