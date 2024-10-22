# pyelternportal

![Project Maintenance][maintenance-shield]
[![GitHub Release][releases-shield]][releases-link]
[![GitHub Activity][commits-shield]][commits-link]
[![License][license-shield]](LICENSE)
[![Code style: black][black-shield]][black-link]

Python client library to retrieve data provided by eltern-portal.org

## Install
```
pip install pyelternportal
```

## Usage by example
Get values
```
import pyelternportal

api = pyelternportal.ElternPortalAPI()
print(f"timezone:\t{api.timezone.zone}")

api.set_config("demo", "demo", "demo")
print(f"school:\t\t{api.school}")
print(f"username:\t{api.username}")

await api.async_validate_config()
print(f"school_name:\t{api.school_name}")

await api.async_update()
print(f"last_update:\t{api.last_update}")

for student in api.students:
    print("---")
    print(f"student_id:\t{student.student_id}")
    print(f"fullname:\t{student.fullname}")
    print(f"firstname:\t{student.firstname}")
    print(f"letters:\t{len(student.letters)}")
    for letter in student.letters:
        print(f"\tnumber:\t\t{letter.number}")
        print(f"\tsent:\t\t{letter.sent}")
        print(f"\tsubject:\t{letter.subject}")
```


[black-link]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge

[commits-link]: https://github.com/michull/pyelternportal/commits/main
[commits-shield]: https://img.shields.io/github/commit-activity/y/michull/pyelternportal.svg?style=for-the-badge

[license-shield]: https://img.shields.io/github/license/michull/pyelternportal?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40michull-blue.svg?style=for-the-badge

[releases-link]: https://github.com/michull/pyelternportal/releases
[releases-shield]: https://img.shields.io/github/release/michull/pyelternportal.svg?style=for-the-badge&include_prereleases
