""" Appointment module """

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Appointment():
    """Class representing an appointment"""
    appointment_id: str
    title: str
    short: str
    classname: str
    start: datetime
    end: datetime
