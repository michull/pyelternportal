""" Substitution module """

from dataclasses import dataclass
from datetime import date

from bs4 import Tag


@dataclass
class Substitution:
    """Class representing a substitution"""
    date: date
    lesson: str
    original_teacher: str
    substitute_teacher: str
    subject_old: str
    subject_new: str
    room: str
    info: str


# Column headers of the substitution plan, the layout differs from school to school
HEADER2KEY = {
    "std": "lesson",
    "betrifft": "original_teacher",
    "vertretung": "substitute_teacher",
    "fach": "subject",
    "raum": "room",
    "info": "info",
}


def tag2columns(headtag: Tag | None) -> dict[str, int] | None:
    """Map the header row of a substitution table to column indexes"""
    if headtag is None:
        return None

    columns = {}
    for index, cell in enumerate(headtag.find_all("td")):
        header = cell.get_text(strip=True).removesuffix(".").lower()
        if header in HEADER2KEY:
            columns[HEADER2KEY[header]] = index

    return columns if "lesson" in columns else None


def cell2text(cells: list[Tag], columns: dict[str, int], key: str) -> str:
    """Text of a cell, empty if the column does not exist"""
    return cells[columns[key]].get_text(strip=True) if key in columns else ""
