from rest_framework import status

from .errors import AuthErrorMessage
from .errors import CognitoErrorMessage


class BaseError(Exception):
    """
    The base error class.
    """

    # The HTTP status code
    status_code = status.HTTP_400_BAD_REQUEST

    app_name = "APP"

    error = None

    # The custom error code
    default_code = ""

    # The developer message about the error
    default_dev_msg = None

    # The friendly user message about the error
    default_user_message = "Something went wrong. Please try again."

    # A flag to determine this error will be sent back in response data or not.
    is_as_response = True

    def __init__(self, code=None, user_message=None, developer_message=None):
        """
        Initialize the exception.

        Args:
            code (str, optional): Error code. Defaults to None.
            user_message (str, optional): User error message. Defaults to None.
            developer_message (str, optional): Developer error message. Defaults to None.
        """
        Exception.__init__(self)

        self.developer_message = developer_message
        self.user_message = user_message
        self.code = code if code is not None else self.default_code

        # Set default message
        default_message = self.default_dev_msg = (
            f"{self.app_name.replace('_', ' ').capitalize()} API is not working properly."
        )

        if not self.default_dev_msg:
            self.default_dev_msg = default_message

        if not self.default_user_message:
            self.default_user_message = default_message

        if not developer_message:
            self.developer_message = self.default_dev_msg or self.who_am_i()

        if not user_message:
            if self.error and self.code:
                self.user_message = getattr(self.error, self.code)
            else:
                self.user_message = self.default_user_message

    def who_am_i(self) -> str:
        """
        Get the name of the exception class.

        @return: The name of the exception class.
        """
        return type(self).__name__

    def to_dict(self):
        """
        Convert the exception to a dictionary.

        @return: The dictionary.
        """
        return {
            "errors": {
                "developer_message": self.developer_message,
                "message": self.user_message,
                "code": f"ERR_{self.app_name}_{self.code}" if self.code else self.app_name,
            },
        }


class UnauthorizedError(BaseError):
    """
    Exception raised when a user tries to sign up with
    a phone number that already
    """

    app_name = "AUTH"
    status_code = status.HTTP_401_UNAUTHORIZED
    error = AuthErrorMessage


class CognitoError(BaseError):
    """
    Cognito exception
    """

    app_name = "COGNITO"
    error = CognitoErrorMessage
    status_code = status.HTTP_400_BAD_REQUEST


class AuthError(BaseError):
    """
    Auth exception
    """

    app_name = "AUTH"
    error = AuthErrorMessage
    status_code = status.HTTP_400_BAD_REQUEST
