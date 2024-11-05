"""Elternprotal API"""

from __future__ import annotations

# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-statements

version = "0.0.14"
version_info = (0, 0, 14)

import datetime
import json
import logging
import re
import socket
from typing import Any, Dict
import urllib.parse

import aiohttp
import bs4
import pytz

from .const import (
    DEFAULT_REGISTER_SHOW_EMPTY,
    DEFAULT_REGISTER_START_MAX,
    DEFAULT_REGISTER_START_MIN,
    SCHOOL_SUBJECTS,
)

from .exception import (
    BadCredentialsException,
    CannotConnectException,
    StudentListException,
    ResolveHostnameException,
)

from .school import School
from .schools import SCHOOLS

from .appointment import Appointment
from .attachment import Attachment, tag2attachment
from .blackboard import BlackBoard
from .lesson import Lesson
from .letter import Letter
from .message import Message
from .poll import Poll
from .student import Student
from .register import Register
from .sicknote import SickNote

from .demo import (
    DEMO_HTML_BASE,
    DEMO_HTML_BLACKBOARD,
    DEMO_HTML_LESSON,
    DEMO_HTML_LETTER,
    DEMO_HTML_LOGIN,
    DEMO_HTML_LOGOUT,
    DEMO_HTML_MESSAGE,
    DEMO_HTML_MESSAGE_TEACHER,
    DEMO_HTML_MESSAGE_DETAIL,
    DEMO_HTML_POLL,
    DEMO_HTML_POLL_DETAIL,
    DEMO_HTML_REGISTER,
    DEMO_HTML_SICKNOTE,
    DEMO_JSON_APPOINTMENT,
)

_LOGGER = logging.getLogger(__name__)

type ConfigType = Dict[str, str]
type OptionType = Dict[str, Any]


class ElternPortalAPI:
    """API to retrieve the data."""

    def __init__(self):
        """Initialize the API."""

        self._timezone = pytz.timezone("Europe/Berlin")
        self._beautiful_soup_parser = "html5lib"

        # set_config
        self.school: str = None
        self.username: str = None
        self.password: str = None
        self.hostname: str = None
        self.base_url: str = None

        # set_option
        self.appointment: bool = False
        self.blackboard: bool = False
        self.lesson: bool = False
        self.letter: bool = False
        self.message: bool = False
        self.poll: bool = False
        self.register: bool = False
        self.sicknote: bool = False

        # set_option_register
        self.register_start_min: int = DEFAULT_REGISTER_START_MIN
        self.register_start_max: int = DEFAULT_REGISTER_START_MAX
        self.register_show_empty: bool = DEFAULT_REGISTER_SHOW_EMPTY

        # async_validate_config
        self._ip: str = None
        self._session: aiohttp.ClientSession = None
        self._csrf: str = None
        self.school_name: str = None

        # other
        self._demo: bool = False
        self._student: Student = None
        self.students: list[Student] = []
        self.last_update = None

    def set_config(self, school: str, username: str, password: str):
        """Initialize the config."""
        school = (
            school.lower()
            .strip()
            .removeprefix("https://")
            .removeprefix("http://")
            .removesuffix("/")
            .removesuffix(".eltern-portal.org")
        )

        if not re.match(r"^[A-Za-z0-9]{1,10}$", school):
            message = '"school" is wrong: one to ten alpha-numeric characters'
            raise BadCredentialsException(message)

        username = username.lower().strip()
        password = password.strip()
        hostname = school + ".eltern-portal.org"
        base_url = "https://" + hostname + "/"

        self._demo = school == "demo"
        self.school = school
        self.username = username
        self.password = password
        self.hostname = hostname
        self.base_url = base_url

    def set_config_data(self, config: ConfigType) -> None:
        """Initialize the config data."""

        school = config.get("school")
        username = config.get("username")
        password = config.get("password")
        self.set_config(school, username, password)

    def set_option(
        self,
        appointment: bool = False,
        blackboard: bool = False,
        lesson: bool = False,
        letter: bool = False,
        message: bool = False,
        poll: bool = False,
        register: bool = False,
        sicknote: bool = False,
    ) -> None:
        """Initialize the option."""

        self.appointment = appointment
        self.blackboard = blackboard
        self.lesson = lesson
        self.letter = letter
        self.message = message
        self.poll = poll
        self.register = register
        self.sicknote = sicknote

    def set_option_data(self, option: OptionType) -> None:
        """Initialize the option data."""

        appointment: bool = option.get("appointment", False)
        blackboard: bool = option.get("blackboard", False)
        lesson: bool = option.get("lesson", False)
        letter: bool = option.get("letter", False)
        message: bool = option.get("message", False)
        poll: bool = option.get("poll", False)
        register: bool = option.get("register", False)
        sicknote: bool = option.get("sicknote", False)

        register_start_min: int = option.get(
            "register_start_min", DEFAULT_REGISTER_START_MIN
        )
        register_start_max: int = option.get(
            "register_start_max", DEFAULT_REGISTER_START_MAX
        )
        register_show_empty: int = option.get(
            "register_show_empty", DEFAULT_REGISTER_SHOW_EMPTY
        )

        self.set_option(
            appointment, blackboard, lesson, letter, message, poll, register, sicknote
        )
        self.set_option_register(
            register_start_min, register_start_max, register_show_empty
        )

    def set_option_register(
        self,
        register_start_min: int = DEFAULT_REGISTER_START_MIN,
        register_start_max: int = DEFAULT_REGISTER_START_MAX,
        register_show_empty: bool = DEFAULT_REGISTER_SHOW_EMPTY,
    ) -> None:
        """Initialize the option register."""

        self.register_start_min = register_start_min
        self.register_start_max = register_start_max
        self.register_show_empty = register_show_empty

    async def async_validate_config(self) -> None:
        """Function validate configuration."""
        if self._demo:
            await self.async_validate_config_demo()
        else:
            await self.async_validate_config_online()

    async def async_validate_config_demo(self) -> None:
        """Function validate configuration (demo)."""

        # base
        self._ip = "127.0.0.1"

        await self.async_base_demo()
        await self.async_login_demo()
        await self.async_logout_demo()
        return

    async def async_validate_config_online(self) -> None:
        """Function validate configuration (online)."""
        _LOGGER.debug("Try to resolve hostname %s", self.hostname)
        try:
            self._ip = socket.gethostbyname(self.hostname)
        except socket.gaierror as sge:
            message = f"Cannot resolve hostname {self.hostname}"
            _LOGGER.exception(message)
            raise ResolveHostnameException(message) from sge
        _LOGGER.debug("IP address is %s", self._ip)

        async with aiohttp.ClientSession(self.base_url) as self._session:
            await self.async_base_online()
            await self.async_login_online()
            await self.async_logout_online()

    async def async_update(self) -> None:
        """Elternportal update."""
        if self._demo:
            await self.async_update_demo()
        else:
            await self.async_update_online()

    async def async_update_demo(self) -> None:
        """Elternportal update (demo)."""

        await self.async_base_demo()
        await self.async_login_demo()

        for self._student in self.students:
            await self.async_set_child_demo()

            if self.appointment:
                await self.async_appointment_demo()

            if self.blackboard:
                await self.async_blackboard_demo()

            if self.lesson:
                await self.async_lesson_demo()

            if self.letter:
                await self.async_letter_demo()

            if self.message:
                await self.async_message_demo()

            if self.poll:
                await self.async_poll_demo()

            if self.register:
                await self.async_register_demo()

            if self.sicknote:
                await self.async_sicknote_demo()

        self._student = None
        await self.async_logout_demo()
        self.last_update = datetime.datetime.now()

    async def async_update_online(self) -> None:
        """Elternportal update (online)."""

        async with aiohttp.ClientSession(self.base_url) as self._session:

            await self.async_base_online()
            await self.async_login_online()

            for self._student in self.students:
                await self.async_set_child_online()

                if self.appointment:
                    await self.async_appointment_online()

                if self.blackboard:
                    await self.async_blackboard_online()

                if self.lesson:
                    await self.async_lesson_online()

                if self.letter:
                    await self.async_letter_online()

                if self.message:
                    await self.async_message_online()

                if self.poll:
                    await self.async_poll_online()

                if self.register:
                    await self.async_register_online()

                if self.sicknote:
                    await self.async_sicknote_online()

            self._student = None
            await self.async_logout_online()
            self.last_update = datetime.datetime.now()

    async def async_base_demo(self) -> None:
        """Elternportal base (demo)."""

        await self.async_base_parse(DEMO_HTML_BASE)

    async def async_base_online(self) -> None:
        """Elternportal base (online)."""

        url = "/"
        _LOGGER.debug("base.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                message = f"base.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            if "Dieses Eltern-Portal existiert nicht" in html:
                message = f"The elternportal {self.base_url} does not exist."
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            await self.async_base_parse(html)

    async def async_base_parse(self, html: str) -> None:
        """Elternportal base (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        try:
            tag = soup.find("input", {"name": "csrf"})
            csrf = tag["value"]
            self._csrf = csrf
        except TypeError as te:
            message = "The 'input' tag with the name 'csrf' could not be found."
            _LOGGER.exception(message)
            raise CannotConnectException(message) from te

        try:
            tag = soup.find("h2", {"id": "schule"})
            school_name = tag.get_text()
            self.school_name = school_name
        except TypeError as te:
            message = "The 'h2' tag with the id 'schule' could not be found."
            _LOGGER.exception(message)
            raise CannotConnectException(message) from te

    async def async_login_demo(self) -> None:
        """Elternportal login (demo)."""

        await self.async_login_parse(DEMO_HTML_LOGIN)

    async def async_login_online(self) -> None:
        """Elternportal login (online)."""

        url = "/includes/project/auth/login.php"
        _LOGGER.debug("login.url=%s", url)
        login_data = {
            "csrf": self._csrf,
            "username": self.username,
            "password": self.password,
            "go_to": "",
        }
        async with self._session.post(url, data=login_data) as response:
            if response.status != 200:
                message = f"login.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            await self.async_login_parse(html)

    async def async_login_parse(self, html: str) -> None:
        """Elternportal login (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        tag = soup.select_one(".pupil-selector")
        if tag is None:
            message = "The tag with class 'pupil-selector' could not be found."
            raise BadCredentialsException(message)

        self.students = []
        tags = soup.select(".pupil-selector select option")
        if not tags:
            message = "The select options could not be found."
            raise StudentListException(message)

        for tag in tags:
            try:
                student_id = tag["value"]
            except Exception as e:
                message = "The 'value' atrribute of a pupil option could not be found."
                raise StudentListException() from e

            try:
                fullname = tag.get_text().strip()
            except Exception as e:
                message = "The 'text' of a pupil option could not be found."
                raise StudentListException() from e

            self._student = Student(student_id, fullname)
            self.students.append(self._student)

    async def async_set_child_demo(self) -> None:
        """Elternportal set child (demo)."""

    async def async_set_child_online(self) -> None:
        """Elternportal set child (online)."""

        url = "/api/set_child.php?id=" + self._student.student_id
        _LOGGER.debug("set_child.url=%s", url)
        async with self._session.post(url) as response:
            if response.status != 200:
                _LOGGER.debug("set_child.status=%s", response.status)

    async def async_appointment_demo(self) -> None:
        """Elternportal appointment (demo)."""

        await self.async_appointment_parse(json.loads(DEMO_JSON_APPOINTMENT))

    async def async_appointment_online(self) -> None:
        """Elternportal appointment (online)."""

        url = "/api/ws_get_termine.php"
        _LOGGER.debug("appointment.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("appointment.status=%s", response.status)

            # process malformed JSON response with parameter content_type
            appointments = await response.json(content_type="text/html")
            await self.async_appointment_parse(appointments)

    async def async_appointment_parse(self, appointments: Any) -> None:
        """Elternportal appointment (parse)."""

        self._student.appointments = []
        if appointments["success"] == 1:
            for result in appointments["result"]:
                start = int(str(result["start"])[0:-3])
                start = datetime.datetime.fromtimestamp(start, self._timezone).date()
                end = int(str(result["end"])[0:-3])
                end = datetime.datetime.fromtimestamp(end, self._timezone).date()

                appointment = Appointment(
                    result["id"],
                    result["title"],
                    result["title_short"],
                    result["class"],
                    start,
                    end,
                )
                self._student.appointments.append(appointment)

    async def async_blackboard_demo(self) -> None:
        """Elternportal blackboard (demo)."""
        await self.async_blackboard_parse(DEMO_HTML_BLACKBOARD)

    async def async_blackboard_online(self) -> None:
        """Elternportal blackboard (online)."""

        url = "/aktuelles/schwarzes_brett"
        _LOGGER.debug("blackboard.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("blackboard.status=%s", response.status)
            html = await response.text()
            await self.async_blackboard_parse(html)

    async def async_blackboard_parse(self, html: str) -> None:
        """Elternportal blackboard."""

        self._student.blackboards = []
        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        tags = soup.select("#asam_content .grid .grid-item .well")
        for tag in tags:
            # sent
            sent = None
            p1 = tag.select_one("p:nth-child(1)")
            if p1:
                match = re.search(
                    r"eingestellt am (\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})",
                    p1.get_text(),
                )
                if match:
                    sent = datetime.datetime.strptime(match[1], "%d.%m.%Y").date()

            # subject
            h4 = tag.select_one("h4:nth-child(2)")
            subject = h4.get_text() if h4 else None

            # body
            p2 = tag.select_one("p:nth-child(3)")
            body = p2.get_text() if p2 else None

            # attachment
            a = tag.select_one("p:nth-child(4) a")
            attachment: Attachment = tag2attachment(a) if a else None

            blackboard = BlackBoard(
                sent=sent, subject=subject, body=body, attachment=attachment
            )
            self._student.blackboards.append(blackboard)

    async def async_lesson_demo(self) -> None:
        """Elternportal lesson (demo)."""

        await self.async_lesson_parse(DEMO_HTML_LESSON)

    async def async_lesson_online(self) -> None:
        """Elternportal lesson (online)."""

        url = "/service/stundenplan"
        _LOGGER.debug("lesson.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("lesson.status=%s", response.status)
            html = await response.text()
            await self.async_lesson_parse(html)

    async def async_lesson_parse(self, html: str) -> None:
        """Elternportal lesson (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        self._student.lessons = []
        table_rows = soup.select("#asam_content div.table-responsive table tr")
        for table_row in table_rows:
            table_cells = table_row.select("td")

            if len(table_cells) == 6:
                # Column 0
                lines = table_cells[0].find_all(string=True)
                number = lines[0] if len(lines) > 0 else ""
                # time = lines[1] if len(lines) > 1 else ""

                # Column 1-5: Monday to Friday
                for weekday in range(1, 6):
                    span = table_cells[weekday].select_one("span span")
                    if span:
                        lines = span.find_all(string=True)
                        subject = lines[0].strip() if len(lines) > 0 else ""
                        room = lines[1].strip() if len(lines) > 1 else ""

                        if subject != "":
                            lesson = Lesson(weekday, number, subject, room)
                            self._student.lessons.append(lesson)

    async def async_letter_demo(self) -> None:
        """Elternportal letter (demo)."""
        await self.async_letter_parse(DEMO_HTML_LETTER)

    async def async_letter_online(self) -> None:
        """Elternportal letter (online)."""

        url = "/aktuelles/elternbriefe"
        _LOGGER.debug("letter.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("letter.status=%s", response.status)
            html = await response.text()
            await self.async_letter_parse(html)

    async def async_letter_parse(self, html: str) -> None:
        """Elternportal letter."""

        self._student.letters = []
        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        tags = soup.select(".link_nachrichten")
        for tag in tags:
            # letter id
            match = re.search(r"\d+", tag.get("onclick"))
            letter_id = match[0] if match else None

            # attachment
            attachment = tag.name == "a"

            # sent
            match = re.search(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}", tag.get_text())
            if match is None:
                sent = None
            else:
                try:
                    sent = datetime.datetime.strptime(match[0], "%d.%m.%Y %H:%M:%S")
                    sent = self._timezone.localize(sent)
                except ValueError:
                    sent = None

            # new + number
            cell = soup.find("td", {"id": "empf_" + letter_id})
            if cell is None:
                new = True
                number = "???"
            else:
                new = cell.get_text() == "Empfang noch nicht bestätigt."
                cell2 = cell.find_previous_sibling()
                if cell2 is None:
                    number = "???"
                else:
                    number = cell2.get_text()

            # subject
            cell = tag.find("h4")
            subject = cell.get_text() if cell else None

            # distribution + description
            cell = tag.parent
            if cell is None:
                distribution = None
                description = None
            else:
                span = cell.select_one("span[style='font-size: 8pt;']")
                if span is None:
                    distribution = None
                else:
                    text = span.get_text()
                    liste = text.split("Klasse/n: ")
                    liste = [x for x in liste if x]
                    distribution = ", ".join(liste)

                lines = cell.find_all(string=True)
                description = ""
                skip = True
                for line in lines:
                    if not skip:
                        description += line.replace("\r", "").replace("\n", "") + "\n"
                    if line.startswith("Klasse/n: "):
                        skip = False

            letter = Letter(
                letter_id=letter_id,
                number=number,
                sent=sent,
                new=new,
                attachment=attachment,
                subject=subject,
                distribution=distribution,
                description=description,
            )
            self._student.letters.append(letter)

    async def async_message_demo(self) -> None:
        """Elternportal message (demo)."""
        await self.async_message_parse(DEMO_HTML_MESSAGE)

    async def async_message_online(self) -> None:
        """Elternportal message (online)."""

        url = "/meldungen/kommunikation_fachlehrer"
        _LOGGER.debug("message.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("message.status=%s", response.status)
            html = await response.text()
            await self.async_message_parse(html)

    async def async_message_parse(self, html: str) -> None:
        """Elternportal message (parse)."""

        self._student.messages = []
        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        rows = soup.select(
            "#asam_content div.table-responsive:nth-child(2) table.table2 tr"
        )
        for row in rows:
            tag = row.select_one("tr td:nth-child(4) a")
            if tag is None:
                href = None
            else:
                href = urllib.parse.urljoin("/", tag["href"])
                _LOGGER.debug(f"href={href}")

            if href is None:
                pass
            else:
                if self._demo:
                    await self.async_message_teacher_demo()
                else:
                    await self.async_message_teacher_online(href)

    async def async_message_teacher_demo(self) -> None:
        """Elternportal message teacher (demo)."""
        await self.async_message_teacher_parse(DEMO_HTML_MESSAGE_TEACHER)

    async def async_message_teacher_online(self, url) -> None:
        """Elternportal message teacher (online)."""

        _LOGGER.debug("message.teacher.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("message.teacher.status=%s", response.status)
            html = await response.text()
            await self.async_message_teacher_parse(html)

    async def async_message_teacher_parse(self, html: str) -> None:
        """Elternportal message teacher (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        tags = soup.select(
            "#asam_content a.btn.btn-default.btn-block[href^='meldungen/kommunikation_fachlehrer/']"
        )
        for tag in tags:
            href = urllib.parse.urljoin("/", tag["href"])
            _LOGGER.debug(f"href={href}")

            if href is None:
                sender = None
                subject = None
                body = None
            else:
                sent = None
                label = tag.parent.parent.select_one("label")
                if label:
                    match = re.search(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}",label.get_text())
                    if match:
                        sent = datetime.datetime.strptime(match[0], "%d.%m.%Y %H:%M")
                        _LOGGER.debug(f"sent={sent}")

                if self._demo:
                    (sender, subject, body) = await self.async_message_detail_demo()
                else:
                    (sender, subject, body) = await self.async_message_detail_online(href)

                message = Message(
                    sender=sender,
                    sent=sent,
                    subject=subject,
                    body=body,
                )
                self._student.messages.append(message)

    async def async_message_detail_demo(self) -> tuple[str, str, str]:
        """Elternportal message detail (demo)."""
        (sender, subject, body) = await self.async_message_detail_parse(
            DEMO_HTML_MESSAGE_DETAIL
        )
        return (sender, subject, body)

    async def async_message_detail_online(self, url: str) -> tuple[str, str, str]:
        """Elternportal message detail (online)."""

        _LOGGER.debug("message.detail.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("message.detail.status=%s", response.status)
            html = await response.text()

            (sender, subject, body) = await self.async_message_detail_parse(html)
            return (sender, subject, body)

    async def async_message_detail_parse(self, html: str) -> tuple[str, str, str]:
        """Elternportal message detail (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        tag = soup.select_one("#asam_content div.row:nth-child(2) div:nth-child(2)")
        subject = tag.get_text() if tag else None
        _LOGGER.debug(f"subject={subject}")

        tag = soup.select_one("#asam_content div.row label span")
        sender = tag.get_text() if tag else None
        _LOGGER.debug(f"sender={sender}")

        tag = soup.select_one(
            "#asam_content div.row div.form-control.arch_kom"
        )
        body = tag.get_text() if tag else None
        _LOGGER.debug(f"body={body}")
        return (sender, subject, body)

    async def async_poll_demo(self) -> None:
        """Elternportal poll (demo)."""
        await self.async_poll_parse(DEMO_HTML_POLL)

    async def async_poll_online(self) -> None:
        """Elternportal poll (online)."""

        url = "/aktuelles/umfragen"
        _LOGGER.debug("poll.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("poll.status=%s", response.status)
            html = await response.text()
            await self.async_poll_parse(html)

    async def async_poll_parse(self, html: str) -> None:
        """Elternportal poll (parse)."""

        self._student.polls = []
        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        rows = soup.select("#asam_content div.row.m_bot")
        for row in rows:
            tag = row.select_one("div div:nth-child(1) a.umf_list")
            if tag is None:
                title = None
                href = None
            else:
                title = tag.get_text()
                href = urllib.parse.urljoin("/", tag["href"])

            tag = row.select_one("div div:nth-child(1) a[title='Anhang']")
            attachment = tag2attachment(tag) if tag else None

            tag = row.select_one("div div:nth-child(2)")
            if tag is None:
                end = None
            else:
                match = re.search(r"\d{2}\.\d{2}\.\d{4}", tag.get_text())
                if match is None:
                    end = None
                else:
                    end = datetime.datetime.strptime(match[0], "%d.%m.%Y").date()

            tag = row.select_one("div div:nth-child(3)")
            if tag is None:
                vote = None
            else:
                match = re.search(r"\d{2}\.\d{2}\.\d{4}", tag.get_text())
                if match is None:
                    vote = None
                else:
                    vote = datetime.datetime.strptime(match[0], "%d.%m.%Y").date()

            if href is None:
                detail = None
            else:
                if self._demo:
                    detail = await self.async_poll_detail_demo()
                else:
                    detail = await self.async_poll_detail_online(href)

            poll = Poll(
                title=title,
                href=href,
                attachment=attachment,
                vote=vote,
                end=end,
                detail=detail,
            )
            self._student.polls.append(poll)

    async def async_poll_detail_demo(self) -> str:
        """Elternportal poll detail (demo)."""
        detail = await self.async_poll_detail_parse(DEMO_HTML_POLL_DETAIL)
        return detail

    async def async_poll_detail_online(self, url: str) -> str:
        """Elternportal poll detail (online)."""

        _LOGGER.debug("poll.detail.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("poll.detail.status=%s", response.status)
            html = await response.text()
            detail = await self.async_poll_detail_parse(html)
            return detail

    async def async_poll_detail_parse(self, html: str) -> str:
        """Elternportal poll detail (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        div = soup.select_one(
            "#asam_content form.form-horizontal div.form-group:nth-child(3)"
        )
        detail = div.get_text() if div else None
        return detail

    async def async_register_demo(self) -> None:
        """Elternportal register (demo)."""

        self._student.registers = []
        date_current = datetime.date.today()
        await self.async_register_parse(DEMO_HTML_REGISTER, date_current)

    async def async_register_online(self) -> None:
        """Elternportal register (online)."""

        self._student.registers = []
        date_current = datetime.date.today() + datetime.timedelta(
            days=self.register_start_min
        )
        date_until = datetime.date.today() + datetime.timedelta(
            days=self.register_start_max
        )
        while date_current <= date_until:

            url = "/service/klassenbuch?cur_date=" + date_current.strftime("%d.%m.%Y")
            _LOGGER.debug("register.url=%s", url)
            async with self._session.get(url) as response:
                if response.status != 200:
                    _LOGGER.debug("register.status=%s", response.status)
                html = await response.text()
                await self.async_register_parse(html, date_current)

            date_current += datetime.timedelta(days=1)

    async def async_register_parse(
        self, html: str, date_current: datetime.date
    ) -> None:
        """Elternportal register (parse)."""

        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        tables = soup.select("#asam_content table.table.table-bordered")
        for table in tables:
            tag = table.select_one("thead tr th:nth-child(2)")
            content = tag.get_text() if tag else ""
            attachments = []
            subject = None
            short = None
            teacher = None
            lesson = None
            substitution = False
            match = re.search(
                r"(.*) - Lehrkraft: (.*) \((Einzel|Doppel)stunde(, Vertretung)?\)",
                content,
            )
            if match:
                subject = match[1].replace("Fach: ", "")
                teacher = match[2]
                lesson = (
                    match[3].replace("Einzel", "single").replace("Doppel", "double")
                )
                substitution = match[4] is not None

                for school_subject in SCHOOL_SUBJECTS:
                    if school_subject["Name"] == subject:
                        short = school_subject["Short"]

            rtype = None
            description = None
            date_completion = date_current
            empty = False

            rows = table.select("tbody tr")
            for row in rows:
                tag = row.select_one("td:nth-child(1)")
                content = tag.get_text() if tag else ""
                match content:
                    case "Hausaufgabe":
                        tag = row.select_one("td:nth-child(2)")

                        # type
                        rtype = "homework"

                        # date_completion + empty
                        i = tag.find("i")
                        if i:
                            content = i.get_text()
                            match = re.search(
                                r"^Zu Erledigen bis: (\d{2}\.\d{2}\.\d{4})$",
                                content,
                            )
                            if match:
                                date_completion = datetime.datetime.strptime(
                                    match[1], "%d.%m.%Y"
                                ).date()

                            if content == "Keine Hausaufgabe eingetragen.":
                                empty = True

                        # description
                        descriptions = []
                        nodes = tag.findAll(string=True, recursive=False)
                        for node in nodes:
                            if node != "- ":
                                descriptions.append(node)
                        description = "\n".join(descriptions) if descriptions else None

                    case "Datei(e)n":
                        tag = row.select_one("td:nth-child(2)")
                        content = tag.get_text() if tag else ""
                        lines = tag.find_all(string=True)

                        # attachment
                        a = tag.find("a")
                        if a:
                            attachment = tag2attachment(a)

                            match = re.search(r"\((\d+\.\d+) KB\)", lines[2])
                            if match:
                                attachment.size = float(match[1])

                            attachments.append(attachment)

            if self.register_show_empty or not empty or attachments:
                register = Register(
                    subject=subject,
                    short=short,
                    teacher=teacher,
                    lesson=lesson,
                    substitution=substitution,
                    empty=empty,
                    rtype=rtype,
                    start=date_current,
                    completion=date_completion,
                    description=description,
                )
                self._student.registers.append(register)

    async def async_sicknote_demo(self) -> None:
        """Elternportal sick note (demo)."""
        await self.async_sicknote_parse(DEMO_HTML_SICKNOTE)

    async def async_sicknote_online(self) -> None:
        """Elternportal sick note (online)."""

        url = "/meldungen/krankmeldung"
        _LOGGER.debug("sicknote.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("sicknote.status=%s", response.status)
            html = await response.text()
            await self.async_sicknote_parse(html)

    async def async_sicknote_parse(self, html: str) -> None:
        """Elternportal sick note (parse)."""

        self._student.sicknotes = []
        soup = bs4.BeautifulSoup(html, self._beautiful_soup_parser)

        rows = soup.select("#asam_content table.ui.table tr")
        for row in rows:
            cells = row.select("td")

            # link
            try:
                tag = cells[0].find("a")
                link = tag["href"]
            except TypeError:
                link = None

            # query
            result = urllib.parse.urlparse(link)
            query = urllib.parse.parse_qs(result.query)

            # df -> start
            start = None
            if "df" in query:
                df = int(query["df"][0])
                start = datetime.datetime.fromtimestamp(df, self._timezone).date()
            else:
                if len(cells) > 1:
                    lines = cells[1].find_all(string=True)
                    if lines:
                        match = re.search(r"\d{2}\.\d{2}\.\d{4}", lines[0])
                        if match:
                            start = datetime.datetime.strptime(
                                match[0], "%d.%m.%Y"
                            ).date()

            # dt -> end
            end = start
            if "dt" in query:
                dt = int(query["dt"][0])
                end = datetime.datetime.fromtimestamp(dt, self._timezone).date()
            else:
                if len(cells) > 1:
                    lines = cells[1].find_all(string=True)
                    if lines:
                        match = re.search(r"\d{2}\.\d{2}\.\d{4}", lines[1])
                        if match:
                            end = datetime.datetime.strptime(
                                match[0], "%d.%m.%Y"
                            ).date()

            # k -> comment
            comment = None
            if "k" in query:
                comment = str(query["k"][0])
            else:
                if len(cells) > 2:
                    comment = cells[2].get_text()

            if comment == "":
                comment = None
            sicknote = SickNote(start, end, comment)
            self._student.sicknotes.append(sicknote)

    async def async_logout_demo(self) -> None:
        """Elternportal logout (demo)."""

        await self.async_logout_parse(DEMO_HTML_LOGOUT)

    async def async_logout_online(self) -> None:
        """Elternportal logout (online)."""

        url = "/logout"
        _LOGGER.debug("logout.url=%s", url)
        async with self._session.get(url) as response:
            if response.status != 200:
                message = f"logout.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            await self.async_logout_parse(html)

    async def async_logout_parse(self, html: str) -> None:
        """Elternportal logout (online)."""

        # nothing to do

    def get_schools(self) -> list[School]:
        """Elternportal get list of schools."""
        return SCHOOLS
