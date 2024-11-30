""" Attachment module """

from dataclasses import dataclass
from urllib import parse

from bs4 import Tag

ATYPE_DEFAULT = "default"
ATYPE_REGISTER = "lesson"


@dataclass
class Attachment:
    """Class representing an attachment"""
    atype: str
    aid: int
    name: str
    href: str
    size: float


def tag2attachment(atag: Tag) -> Attachment:
    """Convert html tag into class attachment"""
    href = atag["href"] if atag.has_attr("href") else None
    url = parse.urljoin("/", href)
    parseresult = parse.urlparse(url)
    query = parse.parse_qs(parseresult.query)

    match parseresult.path:

        case "/aktuelles/get_file/":
            atype = ATYPE_DEFAULT
            aid = int(query["repo"][0]) if "repo" in query else None
            name = atag["title"] if atag.has_attr("title") else None
            if name == "Anhang":
                name = None
            if name and name[-14:] == " herunterladen":
                name = name[:-14]

        case "/service/get_lesson_file/":
            atype = ATYPE_REGISTER
            aid = int(query["f"][0]) if "f" in query else None
            name = atag.get_text() if atag else None

    return Attachment(
        atype=atype, aid=aid, name=name, href=href, size=None
    )
