""" Elternportal API - exceptions """

class BadCredentialsException(Exception):
    """Error to indicate there are bad credentials."""


class CannotConnectException(Exception):
    """Error to indicate we cannot connect."""


class PupilListException(Exception):
    """Error to indicate there are no pupils."""


class ResolveHostnameException(Exception):
    """Error to indicate we cannot resolve the hostname."""
