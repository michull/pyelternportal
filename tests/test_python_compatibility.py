"""Exercise the public demo API without contacting a school portal."""

import unittest
from unittest.mock import patch

import aiohttp

from pyelternportal import ElternPortalAPI


class PythonCompatibilityTest(unittest.IsolatedAsyncioTestCase):
    async def test_demo_update(self):
        with patch.object(
            aiohttp.ClientSession,
            "_request",
            side_effect=AssertionError("The demo must not make HTTP requests"),
        ):
            async with aiohttp.ClientSession() as session:
                api = ElternPortalAPI(session)
                api.set_config("demo", "", "")
                api.set_option(
                    appointment=True,
                    blackboard=True,
                    lesson=True,
                    letter=True,
                    message=True,
                    poll=True,
                    register=True,
                    sicknote=True,
                    substitution=True,
                )
                await api.async_validate_config()
                self.assertTrue(api.school_name)
                await api.async_update()
                self.assertIsNotNone(api.last_update)
                self.assertTrue(api.students)
                for student in api.students:
                    with self.subTest(student=student.student_id):
                        self.assertTrue(student.student_id)
                        self.assertTrue(student.fullname)
                        self.assertTrue(student.letters)
                        self.assertTrue(student.messages)
                        self.assertTrue(student.substitutions)


if __name__ == "__main__":
    unittest.main()
