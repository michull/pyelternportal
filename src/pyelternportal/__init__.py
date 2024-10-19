"""Elternprotal API"""

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches

from __future__ import annotations

import datetime
import logging
import re
import socket
from typing import Any, Dict, Sequence
import urllib.parse

import aiohttp
import bs4
import pytz

from .const import (
    DEFAULT_REGISTER_START_MAX,
    DEFAULT_REGISTER_START_MIN,
    SCHOOL_SUBJECTS,
)

from .exception import (
    BadCredentialsException,
    CannotConnectException,
    PupilListException,
    ResolveHostnameException,
)

from .appointment import Appointment
from .lesson import Lesson
from .letter import Letter
from .poll import Poll
from .pupil import Pupil
from .register import Register
from .sicknote import SickNote

_LOGGER = logging.getLogger(__name__)

type ConfigType = Dict[str, str]
type OptionType = Dict[str, Any]
type PupilListType = Sequence[Pupil]


class ElternPortalAPI:
    """API to retrieve the data."""

    def __init__(self):
        """Initialize the API."""

        self.timezone = pytz.timezone("Europe/Berlin")
        self.beautiful_soup_parser = "html5lib"

        # set_config
        self.school: str = None
        self.username: str = None
        self.password: str = None
        self.hostname: str = None
        self.base_url: str = None

        # set_option
        self.appointment: bool = False
        self.lesson: bool = False
        self.letter: bool = False
        self.poll: bool = False
        self.register: bool = False
        self.sicknote: bool = False

        # set_option_register
        self.register_start_min: int = DEFAULT_REGISTER_START_MIN
        self.register_start_max: int = DEFAULT_REGISTER_START_MAX

        # async_validate_config
        self.ip: str = None
        self.session: aiohttp.ClientSession = None
        self.csrf: str = None
        self.school_name: str = None

        # other
        self.pupil: Pupil = None
        self.pupils: Sequence[Pupil] = []
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
        lesson: bool = False,
        letter: bool = False,
        poll: bool = False,
        register: bool = False,
        sicknote: bool = False,
    ) -> None:
        """Initialize the option."""

        self.appointment: bool = appointment
        self.lesson: bool = lesson
        self.letter: bool = letter
        self.poll: bool = poll
        self.register: bool = register
        self.sicknote: bool = sicknote

    def set_option_register(
        self,
        register_start_min: int = DEFAULT_REGISTER_START_MIN,
        register_start_max: int = DEFAULT_REGISTER_START_MAX,
    ) -> None:
        """Initialize the option register."""

        self.register_start_min: int = register_start_min
        self.register_start_max: int = register_start_max

    def set_option_data(self, option: OptionType) -> None:
        """Initialize the option data."""

        appointment: bool = option.get("appointment", False)
        lesson: bool = option.get("lesson", False)
        letter: bool = option.get("letter", False)
        poll: bool = option.get("poll", False)
        register: bool = option.get("register", False)
        sicknote: bool = option.get("sicknote", False)

        register_start_min: int = option.get(
            "register_start_min", DEFAULT_REGISTER_START_MIN
        )
        register_start_max: int = option.get(
            "register_start_max", DEFAULT_REGISTER_START_MAX
        )

        self.set_option(appointment, lesson, letter, poll, register, sicknote)
        self.set_option_register(register_start_min, register_start_max)

    async def async_validate_config(self) -> None:
        """Function validate configuration."""
        if self.school == "demo":
            # base
            self.ip = "127.0.0.1"
            self.csrf = "demo"
            self.school_name = "Demo Gymnasium"

            # login
            pupil_id = "demo"
            fullname = "Erika Mustermann (1a)"
            self.pupils = [Pupil(pupil_id, fullname)]
            return

        _LOGGER.debug("Try to resolve hostname %s", self.hostname)
        try:
            self.ip = socket.gethostbyname(self.hostname)
        except socket.gaierror as sge:
            message = f"Cannot resolve hostname {self.hostname}"
            _LOGGER.exception(message)
            raise ResolveHostnameException(message) from sge
        _LOGGER.debug("IP address is %s", self.ip)

        async with aiohttp.ClientSession(self.base_url) as self.session:
            await self.async_base()
            await self.async_login()
            await self.async_logout()

    async def async_update(self) -> None:
        """Elternportal start page."""
        if self.school == "demo":

            pupil_id = "demo"
            fullname = "Erika Mustermann (1a)"
            self.pupil = Pupil(pupil_id, fullname)
            self.pupils = [self.pupil]

            day0 = datetime.datetime.now().date()
            day0 -= datetime.timedelta(days=day0.weekday())
            day1 = day0 + datetime.timedelta(days=1)
            day2 = day0 + datetime.timedelta(days=2)
            day3 = day0 + datetime.timedelta(days=3)
            day4 = day0 + datetime.timedelta(days=4)
            day7 = day0 + datetime.timedelta(days=7)

            # appointment
            self.pupil.appointments = [
                Appointment(
                    appointment_id="id_1",
                    title="Schulaufgabe in Englisch",
                    short="SA in E",
                    classname="event-important",
                    start=day3,
                    end=day3,
                ),
                Appointment(
                    appointment_id="id_2",
                    title="Schulaufgabe in Deutsch",
                    short="SA in D",
                    classname="event-important",
                    start=day7,
                    end=day7,
                ),
            ]

            # lesson
            self.pupil.lessons = []

            # letter
            self.pupil.letters = [
                Letter(
                    letter_id="1",
                    number="#1",
                    sent=datetime.datetime.now(),
                    new=True,
                    attachment=True,
                    subject="1. Klassenelternabend",
                    distribution="1a",
                    description="Liebe Eltern\n\n...\n",
                )
            ]

            # poll
            self.pupil.polls = []

            # register
            self.pupil.registers = [
                Register(
                    subject="Englisch",
                    short="E",
                    teacher="Herr Mustermann",
                    lesson="single",
                    substitution=False,
                    rtype="homework",
                    start=day0,
                    completion=day2,
                    description="Buch S. 123, Aufgaben 1-3",
                ),
                Register(
                    subject="Deutsch",
                    short="D",
                    teacher="Frau Müller",
                    lesson="double",
                    substitution=True,
                    rtype="homework",
                    start=day1,
                    completion=day4,
                    description="Arbeitsheft S. 45, Aufgaben 1 b+c",
                ),
            ]

            # sicknote
            self.pupil.sicknotes = [SickNote(day1, day1, None)]

            self.last_update = datetime.datetime.now()
            return

        async with aiohttp.ClientSession(self.base_url) as self.session:

            await self.async_base()
            await self.async_login()

            for self.pupil in self.pupils:
                await self.async_set_child()

                if self.appointment:
                    await self.async_appointment()

                if self.lesson:
                    await self.async_lesson()

                if self.letter:
                    await self.async_letter()

                if self.poll:
                    await self.async_poll()

                if self.register:
                    await self.async_register()

                if self.sicknote:
                    await self.async_sicknote()

            await self.async_logout()
            self.last_update = datetime.datetime.now()

    async def async_base(self) -> None:
        """Elternportal base."""

        url = "/"
        _LOGGER.debug("base.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                message = f"base.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            if "Dieses Eltern-Portal existiert nicht" in html:
                message = f"The elternportal {self.base_url} does not exist."
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

            try:
                tag = soup.find("input", {"name": "csrf"})
                csrf = tag["value"]
                self.csrf = csrf
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

    async def async_login(self) -> None:
        """Elternportal login."""

        url = "/includes/project/auth/login.php"
        _LOGGER.debug("login.url=%s", url)
        login_data = {
            "csrf": self.csrf,
            "username": self.username,
            "password": self.password,
            "go_to": "",
        }
        async with self.session.post(url, data=login_data) as response:
            if response.status != 200:
                message = f"login.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)

            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

            tag = soup.select_one(".pupil-selector")
            if tag is None:
                raise BadCredentialsException()

            self.pupils = []
            tags = soup.select(".pupil-selector select option")
            if not tags:
                raise PupilListException()

            for tag in tags:
                try:
                    pupil_id = tag["value"]
                except Exception as e:
                    message = (
                        "The 'value' atrribute of a pupil option could not be found."
                    )
                    raise PupilListException() from e

                try:
                    fullname = tag.get_text().strip()
                except Exception as e:
                    message = "The 'text' of a pupil option could not be found."
                    raise PupilListException() from e

                self.pupil = Pupil(pupil_id, fullname)
                self.pupils.append(self.pupil)

    async def async_set_child(self) -> None:
        """Elternportal set child."""

        url = "/api/set_child.php?id=" + self.pupil.pupil_id
        _LOGGER.debug("set_child.url=%s", url)
        async with self.session.post(url) as response:
            if response.status != 200:
                _LOGGER.debug("set_child.status=%s", response.status)

    async def async_appointment(self) -> None:
        """Elternportal appointment."""

        self.pupil.appointments = []
        url = "/api/ws_get_termine.php"
        _LOGGER.debug("appointment.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("appointment.status=%s", response.status)

            # process malformed JSON response with parameter content_type
            json = await response.json(content_type="text/html")
            for result in json["result"]:
                start = int(str(result["start"])[0:-3])
                start = datetime.datetime.fromtimestamp(start, self.timezone).date()
                end = int(str(result["end"])[0:-3])
                end = datetime.datetime.fromtimestamp(end, self.timezone).date()

                appointment = Appointment(
                    result["id"],
                    result["title"],
                    result["title_short"],
                    result["class"],
                    start,
                    end,
                )
                self.pupil.appointments.append(appointment)

    async def async_lesson(self) -> None:
        """Elternportal lesson."""

        self.pupil.lessons = []
        url = "/service/stundenplan"
        _LOGGER.debug("lesson.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("lesson.status=%s", response.status)
            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

            table_rows = soup.select("#asam_content div.table-responsive table tr")
            for table_row in table_rows:
                table_cells = table_row.select("td")

                if len(table_cells) == 6:
                    # Column 0
                    lines = table_cells[0].find_all(string=True)
                    number = lines[0] if len(lines) > 0 else ""
                    # time = lines[1] if len(lines) > 1 else ""

                    # Column 1-5: Monday to Friday
                    for weekday in range(1, 5):
                        span = table_cells[weekday].select_one("span span")
                        if span:
                            lines = span.find_all(string=True)
                            subject = lines[0].strip() if len(lines) > 0 else ""
                            room = lines[1].strip() if len(lines) > 1 else ""

                            if subject != "":
                                lesson = Lesson(weekday, number, subject, room)
                                self.pupil.lessons.append(lesson)

    async def async_letter(self) -> None:
        """Elternportal letter."""

        self.pupil.letters = []
        url = "/aktuelles/elternbriefe"
        _LOGGER.debug("letter.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("letter.status=%s", response.status)
            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

            tags = soup.select(".link_nachrichten")
            for tag in tags:
                # letter id
                match = re.search(r"\d+", tag.get("onclick"))
                letter_id = match[0] if match else None

                # attachment
                attachment = tag.name == "a"

                # sent
                match = re.search(
                    r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}", tag.get_text()
                )
                if match is None:
                    sent = None
                else:
                    try:
                        sent = datetime.datetime.strptime(match[0], "%d.%m.%Y %H:%M:%S")
                        sent = self.timezone.localize(sent)
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
                    for i in range(1, len(lines)):
                        line = lines[i].replace("\r", "").replace("\n", "")
                        if not skip:
                            description += line + "\n"
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
                self.pupil.letters.append(letter)

    async def async_poll(self) -> None:
        """Elternportal poll."""

        self.pupil.polls = []
        url = "/aktuelles/umfragen"
        _LOGGER.debug("poll.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("poll.status=%s", response.status)
            html = await response.text()
            soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

            base_tag = soup.find("base")
            baseurl = base_tag["href"] if base_tag else url

            rows = soup.select("#asam_content div.row.m_bot")
            for row in rows:
                tag = row.select_one("div div:nth-child(1) a.umf_list")
                if tag is None:
                    title = None
                    href = None
                else:
                    title = tag.get_text()
                    href = urllib.parse.urljoin(baseurl, tag["href"])

                tag = row.select_one("div div:nth-child(1) a[title='Anhang']")
                attachment = tag is not None

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
                    async with self.session.get(href) as response2:
                        html2 = await response2.text()
                        soup2 = bs4.BeautifulSoup(html2, self.beautiful_soup_parser)

                        div2 = soup2.select_one(
                            "#asam_content form.form-horizontal div.form-group:nth-child(3)"
                        )
                        detail = div2.get_text() if div2 else None

                poll = Poll(
                    title=title,
                    href=href,
                    attachment=attachment,
                    vote=vote,
                    end=end,
                    detail=detail,
                )
                self.pupil.polls.append(poll)

    async def async_register(self) -> None:
        """Elternportal register."""

        self.pupil.registers = []
        date_current = datetime.date.today() + datetime.timedelta(
            days=self.register_start_min
        )
        date_until = datetime.date.today() + datetime.timedelta(
            days=self.register_start_max
        )
        while date_current <= date_until:

            url = "/service/klassenbuch?cur_date=" + date_current.strftime("%d.%m.%Y")
            _LOGGER.debug("register.url=%s", url)
            async with self.session.get(url) as response:
                if response.status != 200:
                    _LOGGER.debug("register.status=%s", response.status)
                html = await response.text()
                soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

                tags = soup.select("#asam_content table.table.table-bordered")
                for tag in tags:
                    table_cells = tag.select("th")
                    content = table_cells[1].get_text() if len(table_cells) > 1 else ""
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
                            match[3]
                            .replace("Einzel", "single")
                            .replace("Doppel", "double")
                        )
                        substitution = match[4] is not None

                    for school_subject in SCHOOL_SUBJECTS:
                        if school_subject["Name"] == subject:
                            short = school_subject["Short"]

                    table_cells = tag.select("td")
                    rtype = table_cells[0].get_text() if len(table_cells) > 0 else ""
                    rtype = rtype.replace("Hausaufgabe", "homework")

                    lines = table_cells[1].find_all(string=True)
                    description = lines[0] if len(lines) > 0 else ""

                    if description != "Keine Hausaufgabe eingetragen.":
                        date_completion = date_current
                        if len(lines) > 2:
                            match = re.search(r"\d{2}\.\d{2}\.\d{4}", lines[2])
                            if match:
                                date_completion = datetime.datetime.strptime(
                                    match[0], "%d.%m.%Y"
                                ).date()

                        register = Register(
                            subject=subject,
                            short=short,
                            teacher=teacher,
                            lesson=lesson,
                            substitution=substitution,
                            rtype=rtype,
                            start=date_current,
                            completion=date_completion,
                            description=description,
                        )
                        self.pupil.registers.append(register)

            date_current += datetime.timedelta(days=1)

    async def async_sicknote(self) -> None:
        """Elternportal sick note."""

        self.pupil.sicknotes = []
        url = "/meldungen/krankmeldung"
        _LOGGER.debug("sicknote.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                _LOGGER.debug("sicknote.status=%s", response.status)
            html = await response.text()

            soup = bs4.BeautifulSoup(html, self.beautiful_soup_parser)

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
                    start = datetime.datetime.fromtimestamp(df, self.timezone).date()
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
                    end = datetime.datetime.fromtimestamp(dt, self.timezone).date()

                # k -> comment
                comment = None
                if "k" in query:
                    comment = str(query["k"][0])
                else:
                    if len(cells) > 2:
                        comment = cells[2].get_text()

                sicknote = SickNote(start, end, comment)
                self.pupil.sicknotes.append(sicknote)

    async def async_logout(self) -> None:
        """Elternportal logout."""

        url = "/logout"
        _LOGGER.debug("logout.url=%s", url)
        async with self.session.get(url) as response:
            if response.status != 200:
                message = f"logout.status={response.status}"
                _LOGGER.exception(message)
                raise CannotConnectException(message)
