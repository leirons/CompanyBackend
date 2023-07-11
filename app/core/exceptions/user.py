from app.core.exceptions.base import (ConflictException, NotFoundException,
                                  UnauthorizedException)
from app.resources.strings import (UserDoesNotFoundMessage,
                               UserWithSameEmailExistsMessage,
                               UserWithSameLoginExistsMessage,
                               UserWithSamePhoneExistsMessage)


class UserWithSameEmailExists(ConflictException):
    message = UserWithSameEmailExistsMessage


class UserWithSameLoginExists(ConflictException):
    message = UserWithSameLoginExistsMessage


class UserWithSamePhoneExists(ConflictException):
    message = UserWithSamePhoneExistsMessage


class UserDoesNotExists(NotFoundException):
    message = UserDoesNotFoundMessage


class PasswordOrLoginDoesNotMatch(UnauthorizedException):
    pass
