""" Elternportal API - exceptions """

class BadCredentialsException(Exception):
    """Error to indicate there are bad credentials."""


class CannotConnectException(Exception):
    """Error to indicate we cannot connect."""


class StudentListException(Exception):
    """Error to indicate there are no students."""


class ResolveHostnameException(Exception):
    """Error to indicate we cannot resolve the hostname."""
