"""Fetch message-list counts without opening messages or downloading attachments.

Only login, child selection, message-list GETs and logout are used. The server
still observes a login and changes its active-child session context. No claim
about undocumented server-side behaviour is made beyond this request contract.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

from . import ElternPortalAPI
from .exception import CannotConnectException, StudentListException

_LOGGER = logging.getLogger(__name__)


class PortalLayoutError(CannotConnectException):
    """The authenticated message list is absent or cannot be counted reliably."""


@dataclass(frozen=True, slots=True)
class ChildMessageCount:
    """Count of distinct rows currently listed for one child, not unread count."""

    student_id: str
    name: str
    count: int


@dataclass(frozen=True, slots=True)
class MessageCounts:
    """A complete account snapshot; a failed child invalidates the snapshot."""

    school: str
    school_name: str
    children: tuple[ChildMessageCount, ...]


def normalize_school(value: str) -> str:
    """Accept the school codes supported by the base client or HTTPS URLs."""
    value = value.strip().lower()
    if "://" in value or "." in value:
        parsed = urlparse(value if "://" in value else "https://" + value)
        host = parsed.hostname or ""
        if (
            parsed.scheme != "https"
            or parsed.username
            or parsed.password
            or parsed.port is not None
            or not host.endswith(".eltern-portal.org")
        ):
            raise ValueError("Enter a school code or an HTTPS Eltern-Portal URL")
        value = host.removesuffix(".eltern-portal.org")
    if re.fullmatch(r"[a-z0-9]{1,11}", value) is None:
        raise ValueError("Invalid school code")
    return value


def parse_message_count(markup: str) -> int:
    """Count distinct thread IDs, rejecting login pages and malformed rows."""
    soup = BeautifulSoup(markup, "html.parser")
    table = soup.select_one("#messages-fachlehrer-table")
    if table is None or table.find("tbody") is None:
        raise PortalLayoutError("Message list was not found")
    identifiers: set[tuple[str, str]] = set()
    for row in table.select("tbody tr"):
        if "message-row" not in row.get("class", []):
            if row.select_one("td.dataTables_empty") is not None:
                continue
            raise PortalLayoutError("Unexpected row in message list")
        match = re.fullmatch(
            r"\s*showMessageFachlehrer\((\d+),\s*(\d+)\);?\s*",
            row.get("onclick", ""),
        )
        if match is None or len(row.find_all("td", recursive=False)) < 4:
            raise PortalLayoutError("Message row layout was not recognized")
        identifiers.add((match[1], match[2]))
    return len(identifiers)


class MessageCountClient(ElternPortalAPI):
    """Small account client using an injected, account-isolated HTTP session."""

    def __init__(
        self, session: aiohttp.ClientSession, school: str, username: str, password: str
    ) -> None:
        super().__init__(session)
        self.set_config(normalize_school(school), username, password)

    async def async_fetch_message_counts(self) -> MessageCounts:
        """Fetch all children atomically; close the portal session on errors."""
        logged_in = False
        try:
            if self._demo:
                from .demo import DEMO_HTML_MESSAGE

                await self.async_base_demo()
                await self.async_login_demo()
            else:
                await self.async_base_online()
                await self.async_login_online()
            logged_in = True
            if not self.students:
                raise StudentListException("No children returned")
            counts: list[ChildMessageCount] = []
            seen: set[str] = set()
            for child in self.students:
                if not child.student_id or child.student_id in seen:
                    raise StudentListException("Missing or duplicate child identifier")
                seen.add(child.student_id)
                self._student = child
                if self._demo:
                    markup = DEMO_HTML_MESSAGE
                else:
                    # Use an explicit status check, rather than the base method
                    # which only logs failed child switches and can mix children.
                    async with self._session.post(
                        f"{self.base_url}api/set_child.php",
                        params={"id": child.student_id},
                    ) as response:
                        response.raise_for_status()
                    async with self._session.get(
                        f"{self.base_url}meldungen/kommunikation_fachlehrer"
                    ) as response:
                        response.raise_for_status()
                        markup = await response.text()
                counts.append(
                    ChildMessageCount(
                        child.student_id, child.fullname, parse_message_count(markup)
                    )
                )
            return MessageCounts(
                self.school, self.school_name or self.school, tuple(counts)
            )
        finally:
            self._student = None
            if logged_in and not self._demo:
                try:
                    await self.async_logout_online()
                except (aiohttp.ClientError, TimeoutError, CannotConnectException):
                    _LOGGER.debug("Portal logout failed after message-list fetch")
