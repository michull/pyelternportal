""" Black board module """

import dataclasses
import datetime

from pyelternportal.attachment import Attachment

@dataclasses.dataclass
class BlackBoard():
    """Class representing a black board"""
    sent: datetime.date
    new: bool
    subject: str
    body: str
    attachment: Attachment
