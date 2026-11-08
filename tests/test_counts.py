"""Minimal Core-facing request contract, using synthetic/demo HTML only."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import aiohttp
import pytest

from pyelternportal.counts import (
    MessageCountClient,
    PortalLayoutError,
    normalize_school,
    parse_message_count,
)
from pyelternportal.exception import BadCredentialsException, StudentListException

ROW = '<tr class="message-row" onclick="showMessageFachlehrer(1, 2)"><td>A</td><td></td><td>Title</td><td>Date</td></tr>'
TABLE = '<table id="messages-fachlehrer-table"><tbody>{}</tbody></table>'


@pytest.mark.parametrize(
    "value,expected",
    [
        (" DEMO ", "demo"),
        ("https://example.eltern-portal.org/login?x=1", "example"),
        ("example.eltern-portal.org", "example"),
        ("school2", "school2"),
    ],
)
def test_normalize_school(value, expected):
    assert normalize_school(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "../x",
        "http://example.eltern-portal.org",
        "example.eltern-portal.org.evil.invalid",
        "a.b.eltern-portal.org",
        "https://u:p@example.eltern-portal.org",
        "https://example.eltern-portal.org:443",
        "https://example.eltern-portal.org:bad",
        "school-2",
        "a" * 12,
        "a" * 64,
        "-example",
    ],
)
def test_normalize_rejects_other_destinations(value):
    with pytest.raises(ValueError):
        normalize_school(value)


def test_count_rows_without_reading_contents():
    assert parse_message_count(TABLE.format("")) == 0
    assert (
        parse_message_count(
            TABLE.format('<tr><td class="dataTables_empty">No messages</td></tr>')
        )
        == 0
    )
    assert parse_message_count(TABLE.format(ROW + ROW)) == 1
    assert parse_message_count(TABLE.format(ROW + ROW.replace("(1, 2)", "(1, 3)"))) == 2
    for markup in [
        "<html>Login</html>",
        TABLE.format(ROW.replace("(1, 2)", "(x, y)")),
        TABLE.format(ROW.replace("<td>A</td>", "")),
        TABLE.format(ROW.replace("message-row", "changed-row")),
        '<table id="messages-fachlehrer-table"></table>',
    ]:
        with pytest.raises(PortalLayoutError):
            parse_message_count(markup)


async def test_demo_never_contacts_network():
    session = Mock(
        get=Mock(side_effect=AssertionError("network")),
        post=Mock(side_effect=AssertionError("network")),
    )
    result = await MessageCountClient(
        session, "demo", "", ""
    ).async_fetch_message_counts()
    assert result.children and all(c.count >= 0 for c in result.children)


def response(markup="", error=None):
    value = Mock()
    value.text = AsyncMock(return_value=markup)
    value.raise_for_status = Mock(side_effect=error)
    context = AsyncMock()
    context.__aenter__.return_value = value
    return context


def online_client(session):
    client = MessageCountClient(session, "example", "user", "pass")
    client.async_base_online = AsyncMock()
    client.async_login_online = AsyncMock()
    client.async_logout_online = AsyncMock()
    client.students = [
        SimpleNamespace(student_id="7", fullname="Child One"),
        SimpleNamespace(student_id="8", fullname="Child Two"),
    ]
    return client


async def test_only_list_endpoint_and_child_switch_are_used():
    session = Mock(
        get=Mock(side_effect=[response(TABLE.format(ROW)), response(TABLE.format(""))]),
        post=Mock(side_effect=[response(), response()]),
    )
    client = online_client(session)
    result = await client.async_fetch_message_counts()
    assert [(c.student_id, c.count) for c in result.children] == [("7", 1), ("8", 0)]
    assert all(
        c.args[0]
        == "https://example.eltern-portal.org/meldungen/kommunikation_fachlehrer"
        for c in session.get.call_args_list
    )
    assert [c.kwargs["params"] for c in session.post.call_args_list] == [
        {"id": "7"},
        {"id": "8"},
    ]
    assert all(
        c.args[0].endswith("/api/set_child.php") for c in session.post.call_args_list
    )
    client.async_logout_online.assert_awaited_once()
    assert client._student is None


@pytest.mark.parametrize("where", ["child", "list", "layout", "second_child"])
async def test_incomplete_account_never_returns_partial_counts(where):
    failure = aiohttp.ClientConnectionError("offline")
    session = Mock(
        post=Mock(
            side_effect=[
                response(error=failure if where == "child" else None),
                response(),
            ]
        ),
        get=Mock(
            side_effect=[
                response(
                    "Login" if where == "layout" else TABLE.format(ROW),
                    failure if where == "list" else None,
                ),
                response(error=failure),
            ]
        ),
    )
    client = online_client(session)
    with pytest.raises((aiohttp.ClientError, PortalLayoutError)):
        await client.async_fetch_message_counts()
    client.async_logout_online.assert_awaited_once()
    assert client._student is None


async def test_invalid_login_does_not_mask_auth_failure():
    client = online_client(Mock())
    client.async_login_online.side_effect = BadCredentialsException("invalid")
    with pytest.raises(BadCredentialsException):
        await client.async_fetch_message_counts()
    client.async_logout_online.assert_not_called()


async def test_logout_failure_keeps_success_and_duplicate_children_fail():
    session = Mock(
        post=Mock(return_value=response()),
        get=Mock(return_value=response(TABLE.format(""))),
    )
    client = online_client(session)
    client.async_logout_online.side_effect = aiohttp.ClientError("logout")
    assert len((await client.async_fetch_message_counts()).children) == 2
    client.students[1].student_id = "7"
    with pytest.raises(StudentListException):
        await client.async_fetch_message_counts()
    client.students = []
    with pytest.raises(StudentListException):
        await client.async_fetch_message_counts()
