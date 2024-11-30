"""School module"""

from dataclasses import dataclass

@dataclass
class School():
    """Dataclass representing a school"""
    school: str = None
    name: str = None
    postcode: str = None
    city: str = None
