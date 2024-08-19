class CognitoErrorMessage:
    """
    Cognito error messages
    """

    INTERNAL_ERROR = ("Cognito internal error.",)
    USER_EXISTS = ("User already exists.",)
    INVALID_PASSWORD = ("Invalid password.",)


class AuthErrorMessage:
    """
    Auth error messages
    """

    SIGN_UP = ("Unable to sign up new account.",)
    LOGIN = ("Unable to login.",)
    INVALID_CREDENTIALS = ("Invalid credentials.",)
    USER_EXISTS = ("User already exists.",)
