""" Letter module """

# pylint: disable=too-many-instance-attributes

import dataclasses
import datetime

@dataclasses.dataclass
class Letter():
    """Class representing a letter"""
    letter_id: str
    number: str
    sent: datetime.datetime
    new: bool
    attachment: bool
    subject: str
    distribution: str
    body: str
