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

## Demo school

With the school identifier "demo" you can try out the library without access data.


## Example
Get the letters of the demo school.
```
import pyelternportal

api = pyelternportal.ElternPortalAPI()
api.set_config("demo", "", "")
api.set_option(letter=True)
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

## API


### Methods

| Method                                                 | Description
| :----------------------------------------------------- | :----------
| `set_config`, `set_config_data`                        | Set the base configuration
| `set_option`, `set_option_register`, `set_option_data` | Set the optional configuration
| `async_validate_config`                                | Validate base config, set property `school_name`
| `async_update`                                         | Update data, set properties `students` and `last_update`


#### `set_config`

Set the required configuration.

| Parameter  | Type  | Description
| :--------- | :---- | :----------
| `school`   | `str` | School identifier for Eltern-Portal. A list of valid school identifiers can be found at [SCHOOLS.MD](schools/SCHOOLS.MD)
| `username` | `str` | User name of the access data (e.g. e-mail address)
| `password` | `str` | Password of the access data


#### `set_config_data`

Set the base configuration via a dictionary object.

| Parameter  | Type             | Description
| :--------- | :--------------- | :----------
| `config`   | `Dict[str, str]` | The dictionary keys corresponds to the parameter names of `set_config`.


#### `set_option`

Set the optional configuration.

| Parameter     | Type   | Default | Description
| :------------ | :----  | :------ | :----------
| `appointment` | `bool` | `False` | Get data of page "service/termine"?
| `blackboard`  | `bool` | `False` | Get data of page "aktuelles/schwarzes_brett"?
| `lesson`      | `bool` | `False` | Get data of page "service/stundenplan"?
| `letter`      | `bool` | `False` | Get data of page "aktuelles/elternbriefe"?
| `poll`        | `bool` | `False` | Get data of page "aktuelles/umfragen"?
| `register`    | `bool` | `False` | Get data of page "service/klassenbuch"?
| `sicknote`    | `bool` | `False` | Get data of page "meldungen/krankmeldung"?


#### `set_option_register`

Set the optional configuration for class register.

| Parameter             | Type   | Default | Description
| :-------------------- | :----- | :-----: | :----------
| `register_start_min`  | `int`  |   -6    | Start date (relative to today) (minimum)
| `register_start_max`  | `int`  |   +5    | Start date (relative to today) (maximum)
| `register_show_empty` | `bool` | `False` | Show empty entries?


#### `set_option_data`

Set the option data via a dictionary object. 

| Parameters | Type             | Description
| :--------- | :--------------- | :----------
| `config`   | `Dict[str, Any]` | The dictionary keys correspond to the parameter names of `set_option` and `set_option_register`.


### Properties

| Property      | Type                | Description
| :------------ | :------------------ | :----------
| `school_name` | `str`               | Name of the school presented on the welcome page
| `students`    | `list[Student]`     | List of students (or pupils)
| `last_update` | `datetime.datetime` | Timestamp of the last update of the data above


## Classes

### Student

| Property       | Type                | Description
| :------------- | :------------------ | :----------
| `student_id`   | `str`               | Id of the student
| `fullname`     | `str`               | Full name of the student presented in the drop down list
| `firstname`    | `str`               | First name (extracted from `fullname`)
| `lastname`     | `str`               | Last name (extracted from `fullname`)
| `classname`    | `str`               | Class name (extracted from `fullname`)
| `appointments` | `list[Appointment]` | List of appointments (only if option `appointment` was set)
| `blackboards`  | `list[BlackBoard]`  | List of black board entries (only if option `blackboard` was set)
| `lessons`      | `list[Lesson]`      | List of lessons (only if option `lesson` was set)
| `letters`      | `list[Letter]`      | List of letters (only if option `letter` was set)
| `polls`        | `list[Poll]`        | List of polls (only if option `poll` was set)
| `registers`    | `list[Register]`    | List of registers (only if option `register` was set)
| `sicknotes`    | `list[SickNote]`    | List of sick notes (only if option `sicknote` was set)


### Appointment

| Property         | Type            | Description
| :--------------- | :-------------- | :----------
| `appointment_id` | `str`           | Id of the appointment
| `title`          | `str`           | Title
| `short`          | `str`           | Short title
| `classname`      | `str`           | Class name
| `start`          | `datetime.date` | Start (including)
| `end`            | `datetime.date` | End (including)

### BlackBoard

| Property     | Type            | Description
| :----------- | :-------------- | :----------
| `sent`       | `datetime.date` | Publication date
| `subject`    | `str`           | Subject
| `body`       | `str`           | Body
| `attachment` | `Attachment`    | Attachment

### Lesson

| Property  | Type  | Description
| :-------- | :---- | :----------
| `weekday` | `int` | 1=Monday ... 5=Friday
| `number`  | `str` | Sequence number
| `subject` | `str` | Subject
| `room`    | `str` | Room

### Letter

| Property       | Type                | Description
| :------------- | :------------------ | :----------
| `letter_id`    | `str`               | Id of the letter
| `number`       | `str`               | Number
| `sent`         | `datetime.datetime` | Publication date and time
| `new`          | `bool`              | Is it new (or has it already been read)?
| `attachment`   | `bool`              | Has attachment?
| `subject`      | `str`               | Subject
| `distribution` | `str`               | Distribution
| `description`  | `str`               | Description

### Poll

| Property     | Type                | Description
| :----------- | :------------------ | :----------
| `title`      | `str`               | Title
| `href`       | `str`               | Link to details
| `attachment` | `bool`              | Has attachment
| `vote`       | `datetime.datetime` | Vote date and time
| `end`        | `datetime.datetime` | End date and time of runtime
| `detail`     | `str`               | Details

### Register

| Property       | Type            | Description
| :------------- | :-------------- | :----------
| `subject`      | `str`           | Subject
| `short`        | `str`           | Short subject
| `teacher`      | `str`           | Teacher
| `lesson`       | `str`           | Lesson
| `substitution` | `bool`          | Was a substitution?
| `empty`        | `bool`          | Is empty?
| `rtype`        | `str`           | Type of register
| `start`        | `datetime.date` | Start date (including)
| `completion`   | `datetime.date` | Complete by date (including)
| `description`  | `str`           | Description


### SickNote

| Property  | Type            | Description
| :-------- | :-------------- | :----------
| `start`   | `datetime.date` | Start date
| `end`     | `datetime.date` | End date
| `comment` | `str`           | Comment


### Attachment

| Property  | Type    | Description
| :-------- | :-------| :----------
| `atype`   | `str`   | Type of attachment: `default` or `lesson`
| `aid`     | `int`   | Id of attachment
| `name`    | `str`   | Name
| `href`    | `str`   | Link
| `size`    | `float` | Size in KB



[black-link]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge

[commits-link]: https://github.com/michull/pyelternportal/commits/main
[commits-shield]: https://img.shields.io/github/commit-activity/y/michull/pyelternportal.svg?style=for-the-badge

[license-shield]: https://img.shields.io/github/license/michull/pyelternportal?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40michull-blue.svg?style=for-the-badge

[releases-link]: https://github.com/michull/pyelternportal/releases
[releases-shield]: https://img.shields.io/github/release/michull/pyelternportal.svg?style=for-the-badge&include_prereleases
