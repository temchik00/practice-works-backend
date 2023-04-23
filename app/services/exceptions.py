from app.exceptions import GeneralException


class ServiceError(GeneralException):
    """
    Exception raised when something went wrong in service
    """


class UnauthorizedError(ServiceError):
    """
    Exception raised when user is unauthorized
    """


class WrongCredentialsError(ServiceError):
    """
    Exception raised when specified credentials are wrong
    i.e. wrong password or expired token
    """


class NotFoundError(ServiceError):
    """
    Exception raised when can't find requested entity
    """
