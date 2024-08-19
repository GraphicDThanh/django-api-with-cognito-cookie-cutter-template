"""Define Cognito Client, this file contains all method to connect with Cognito."""

import boto3
from botocore.exceptions import ClientError
from core.exceptions import AuthError
from core.exceptions import CognitoError
from django.conf import settings

from .cognito_interface import CognitoInterface


class RealCognito(CognitoInterface):
    def __init__(self):
        self.client = boto3.client(service_name="cognito-idp", region_name=settings.AWS_REGION)
        self.cognito_exceptions = self.client.exceptions

        self.USER_POOL_ID = settings.COGNITO_USER_POOL_ID
        self.CLIENT_ID = settings.COGNITO_CLIENT_ID

    def create_user(self, username: str, temporary_password: str) -> dict:
        """
        Create a cognito user

        Args:
            username (str): The user email

        Raises:
            AuthError: If error when create user

        Returns:
            Dict: The response from cognito
        """
        try:
            response = self.client.admin_create_user(
                UserPoolId=self.USER_POOL_ID,
                Username=username,
                UserAttributes=[
                    {"Name": "email", "Value": username},
                    {"Name": "email_verified", "Value": "True"},
                ],
                TemporaryPassword=temporary_password,
            )

            # Return cognito sub to save in database
            attributes = response.get("User", {}).get("Attributes")
            for attribute in attributes:
                if attribute["Name"] == "sub":
                    return attribute["Value"]
        except self.cognito_exceptions.UsernameExistsException as e:
            raise CognitoError(code="USER_EXISTS", developer_message=str(e)) from e
        except ClientError as e:
            raise CognitoError(code="INTERNAL_ERROR", developer_message=str(e)) from e

    def set_user_password(self, username, password):
        """
        Set user password

        Args:
            username (str): The username is the email of the user
            password (str): The password to set
        """
        try:
            self.client.admin_set_user_password(
                UserPoolId=self.USER_POOL_ID,
                Username=username,
                Password=password,
                Permanent=True,  # True if the password is permanent
            )
        except self.cognito_exceptions.InvalidPasswordException as e:
            raise CognitoError(code="INVALID_PASSWORD", developer_message=str(e)) from e
        except ClientError as e:
            raise CognitoError(code="INTERNAL_ERROR", developer_message=str(e)) from e

    def admin_login_user(self, username: str, password: str) -> dict:
        """
        Admin login user
        Note: this API is for admin test login user only

        Args:
            email (str): user email
            password (str): user password

        Returns:
            dict: response
        """
        try:
            # Initiate auth request
            response = self.client.admin_initiate_auth(
                UserPoolId=self.USER_POOL_ID,
                ClientId=self.CLIENT_ID,
                AuthFlow="ADMIN_USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                },
            )

            # Extract tokens from the response
            id_token = response["AuthenticationResult"]["IdToken"]
            access_token = response["AuthenticationResult"]["AccessToken"]
            refresh_token = response["AuthenticationResult"]["RefreshToken"]
        except (
            self.cognito_exceptions.NotAuthorizedException,
            self.cognito_exceptions.UserNotFoundException,
        ) as e:
            raise AuthError(code="INVALID_CREDENTIALS", developer_message=str(e)) from e
        except ClientError as e:
            raise CognitoError(code="INTERNAL_ERROR", developer_message=str(e)) from e
        else:
            return {
                "id_token": id_token,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

    def get_user(self, username: str) -> dict:
        """
        Get user from cognito

        Args:
            username (str): The username of the user

        Returns:
            Dict: The user data
        """

        try:
            return self.client.admin_get_user(
                UserPoolId=self.USER_POOL_ID,
                Username=username,
            )
        except self.cognito_exceptions.UserNotFoundException:
            return None
        except ClientError as e:
            raise CognitoError(code="INTERNAL_ERROR", developer_message=str(e)) from e

    # Other methods
    def is_user_existed(self, username: str) -> bool:
        """
        Check if user is existed

        Args:
            email (str): The email of the user

        Returns:
            bool: True if user is existed
        """
        user = self.get_user(username)
        return user is not None
