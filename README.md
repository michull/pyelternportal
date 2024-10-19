# pyelternportal
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

for pupil in api.pupils:
    print("---")
    print(f"pupil_id:\t{pupil.pupil_id}")
    print(f"fullname:\t{pupil.fullname}")
    print(f"firstname:\t{pupil.firstname}")
    print(f"letters:\t{len(pupil.letters)}")
    for letter in pupil.letters:
        print(f"\tnumber:\t\t{letter.number}")
        print(f"\tsent:\t\t{letter.sent}")
        print(f"\tsubject:\t{letter.subject}")
```
