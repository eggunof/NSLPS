from nslps.application_exception import ApplicationException


class UnificationException(ApplicationException):
    """Raised when unification is impossible."""
