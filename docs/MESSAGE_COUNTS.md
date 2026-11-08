# Teacher-message counts

`MessageCountClient` is an optional API. Existing `ElternPortalAPI` callers are unaffected.
It returns an immutable snapshot of each child's stable student ID, display name and
number of distinct teacher-message threads currently listed in the portal.
This is **not an unread count** and does not include letters or blackboard notices.

```python
import asyncio
import os

import aiohttp
from pyelternportal.counts import MessageCountClient


async def main():
    # Use a dedicated session per account. The client logs out of the portal
    # after fetching; the caller owns and closes the HTTP session.
    async with aiohttp.ClientSession() as session:
        client = MessageCountClient(
            session, os.environ["EP_SCHOOL"],
            os.environ["EP_USERNAME"], os.environ["EP_PASSWORD"],
        )
        snapshot = await client.async_fetch_message_counts()
        for child in snapshot.children:
            print(child.student_id, child.name, child.count)


asyncio.run(main())
```

Use `demo` with empty credentials to try the bundled demonstration without network
requests. School identifiers follow the existing base client's format: 1–11
alphanumeric characters. HTTPS Eltern-Portal URLs are also accepted and normalized.
Foreign hosts, non-HTTPS URLs, ports and embedded credentials are rejected.

The request path is limited to the base/login pages, authentication, active-child
selection, teacher-message lists and logout. It does not open message details,
download attachments, send messages, submit sick notes or confirm receipts.
Login and child selection still change the server session. This describes the
client's requests, not undocumented server-side behavior. Do not share one client
or session between concurrent account fetches.

Authentication uses the existing library exceptions. Transport errors propagate;
`PortalLayoutError` (a `CannotConnectException`) reports an unrecognized message list.
An empty/missing child list or duplicate IDs raise `StudentListException`.
Any child failure rejects the entire snapshot rather than returning partial counts.
Successful login is followed by a best-effort logout, including on fetch failure.

# Release preparation

The added source/tests are MIT; the original library remains Unlicense. Both license
files are included in wheel and sdist. The public CI tests Python 3.13/3.14 with
network disabled, enforces 100% line coverage of the new count module, builds both
distributions and checks their source bytes and license metadata.

The optional tag-triggered `publish.yml` workflow builds, tests, attests and publishes
through a PyPI trusted publisher. Before using it, the maintainer must choose and
update the next version in both `pyproject.toml` and `pyelternportal.__init__.VERSION`,
configure the publisher for the actual repository, workflow `publish.yml`, environment
`pypi`, and protect that environment/release tags. The `v...` tag must match the project
version. No release is created by this contribution. An existing release number
must not be reused on PyPI.

A workflow file is not publication evidence: downstream consumers still need the
actual PyPI version, matching public source tag, successful build/publish run and
matching artifact hashes before using the new API in a released integration.
