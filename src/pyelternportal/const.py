"""Elternportal API - constants"""

import logging
from typing import Dict

LOGGER = logging.getLogger(__name__)

DEFAULT_BLACKBOARD_TRESHOLD: int = -7
DEFAULT_LETTER_TRESHOLD: int = -7
DEFAULT_MESSAGE_TRESHOLD: int = -7
DEFAULT_POLL_TRESHOLD: int = 0
DEFAULT_REGISTER_SHOW_EMPTY: bool = False
DEFAULT_REGISTER_START_MIN: int = -6
DEFAULT_REGISTER_START_MAX: int = +5
DEFAULT_REGISTER_TRESHOLD: int = +1
DEFAULT_SICKNOTE_TRESHOLD: int = -7

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
