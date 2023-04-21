from app.exceptions import GeneralException


class CrudError(GeneralException):
    """
    Exception raised when something went wrong in crud operation
    """


class ConstraintError(CrudError):
    """
    Exception raised when constraint violated
    """


class AlreadyExistsError(CrudError):
    """
    Exception raised when unique constraint violated
    """
