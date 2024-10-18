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

try:
    api = ElternPortalAPI("")

    print(f"school_name:\t{api.school_name}")

    for pupil in api.pupils:
        print(f"pupil:\t{pupil}")
except:
    print("Something went wrong!")
```

Result
```
    print(f"school_name:\t\tAsam Gymnasium")
```
