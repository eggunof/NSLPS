from nslps.application_exception import ApplicationException


class FormulaParserException(ApplicationException):
    """Raised when the LLM output string cannot be parsed."""
