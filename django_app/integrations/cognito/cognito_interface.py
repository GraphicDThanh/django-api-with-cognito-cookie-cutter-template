from abc import ABCMeta
from abc import abstractmethod


class CognitoInterface(metaclass=ABCMeta):
    """
    Initialize the Cognito client
    Note: username from data input for all function use as
    - user.uuid on DB side
    - username on cognito side
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def create_user(self, username: str) -> dict:
        """
        Admin create a cognito user
        """

    @abstractmethod
    def get_user(self, username: str) -> dict:
        """
        Admin get user info from cognito
        """

    @abstractmethod
    def admin_login_user(self, username: str, password: str) -> dict:
        """
        Admin login user
        """
