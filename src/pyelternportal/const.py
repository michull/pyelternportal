"""Elternportal API - constants"""

import logging
from typing import Dict

LOGGER = logging.getLogger(__name__)

CONF_APPOINTMENT_CALENDAR: str = "appointment_calendar"
CONF_APPOINTMENT_TRESHOLD_START: str = "appointment_treshold_start"
CONF_APPOINTMENT_TRESHOLD_END: str = "appointment_treshold_end"
CONF_BLACKBOARD_TRESHOLD: str = "blackboard_treshold"
CONF_LETTER_TRESHOLD: str = "letter_treshold"
CONF_MESSAGE_TRESHOLD: str = "message_treshold"
CONF_POLL_TRESHOLD: str = "poll_treshold"
CONF_REGISTER_CALENDAR: str = "register_calendar"
CONF_REGISTER_START_MIN: str = "register_start_min"
CONF_REGISTER_START_MAX: str = "register_start_max"
CONF_REGISTER_SHOW_EMPTY: str = "register_show_empty"
CONF_REGISTER_TRESHOLD: str = "register_treshold"
CONF_SICKNOTE_CALENDAR: str = "sicknote_calendar"
CONF_SICKNOTE_TRESHOLD: str = "sicknote_treshold"
CONF_SUBSTITUTION_TRESHOLD: str = "substitution_treshold"

DEFAULT_APPOINTMENT_CALENDAR: bool = False
DEFAULT_APPOINTMENT_TRESHOLD_END: int = +0
DEFAULT_APPOINTMENT_TRESHOLD_START: int = +14
DEFAULT_BLACKBOARD_TRESHOLD: int = -7
DEFAULT_LETTER_TRESHOLD: int = -7
DEFAULT_MESSAGE_TRESHOLD: int = -7
DEFAULT_POLL_TRESHOLD: int = 0
DEFAULT_REGISTER_CALENDAR: bool = False
DEFAULT_REGISTER_SHOW_EMPTY: bool = False
DEFAULT_REGISTER_START_MIN: int = -6
DEFAULT_REGISTER_START_MAX: int = +5
DEFAULT_REGISTER_TRESHOLD: int = +1
DEFAULT_SICKNOTE_CALENDAR: bool = False
DEFAULT_SICKNOTE_TRESHOLD: int = -7
DEFAULT_SUBSTITUTION_TRESHOLD: int = 0

SCHOOL_SUBJECTS: list[Dict[str, str]] = [
    {"Short": "B", "Name": "Biologie"},
    {"Short": "BcP", "Name": "Biologisch-chemisches Praktikum"},
    {"Short": "C", "Name": "Chemie"},
    {"Short": "D", "Name": "Deutsch"},
    {"Short": "E", "Name": "Englisch"},
    {"Short": "Eth", "Name": "Ethik"},
    {"Short": "Ev", "Name": "Evangelische Religionslehre"},
    {"Short": "F", "Name": "Französisch"},
    {"Short": "G", "Name": "Geschichte"},
    {"Short": "Geo", "Name": "Geographie"},
    {"Short": "Geol", "Name": "Geologie"},
    {"Short": "Gr", "Name": "Griechisch"},
    {"Short": "Inf", "Name": "Informatik"},
    {"Short": "Infang", "Name": "Angewandte Informatik"},
    {"Short": "It", "Name": "Italienisch"},
    {"Short": "K", "Name": "Katholische Religionslehre"},
    {"Short": "Ku", "Name": "Kunst"},
    {"Short": "L", "Name": "Latein"},
    {"Short": "M", "Name": "Mathematik"},
    {"Short": "Mu", "Name": "Musik"},
    {"Short": "NT", "Name": "Natur und Technik"},
    {"Short": "Ph", "Name": "Physik"},
    {"Short": "PhAst", "Name": "Astrophysik"},
    {"Short": "Ru", "Name": "Russisch"},
    {"Short": "S", "Name": "Sport"},
    {"Short": "STheo", "Name": "Sporttheorie"},
    {"Short": "SpG", "Name": "Sozialpraktische Grundbildung"},
    {"Short": "Sk", "Name": "Sozialkunde"},
    {"Short": "Sp", "Name": "Spanisch"},
    {"Short": "SwA", "Name": "Sozialwissenschaftliche Arbeitsfelder"},
    {"Short": "WIn", "Name": "Wirtschaftsinformatik"},
    {"Short": "WR", "Name": "Wirtschaft und Recht"},
]
