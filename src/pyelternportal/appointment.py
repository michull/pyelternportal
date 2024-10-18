""" Appointment module """

import dataclasses
import datetime

@dataclasses.dataclass
class Appointment():
    """Class representing an appointment"""
    appointment_id: str
    title: str
    short: str
    classname: str
    start: datetime.date
    end: datetime.date
