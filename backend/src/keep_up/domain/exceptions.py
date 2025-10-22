class KeepUpException(Exception):
    pass


class UserConflictError(KeepUpException):
    pass


class DomainAlreadyExistsError(KeepUpException):
    pass
