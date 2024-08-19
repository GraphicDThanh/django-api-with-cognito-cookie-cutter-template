from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django_app.core.exceptions import AuthError
from django_app.core.views import BaseModelViewSet
from django_app.core.views import CommonViewSet
from django_app.integrations.cognito.real_cognito import RealCognito
from django_app.users.models import User

from .serializers import SignupRequestSerializer
from .serializers import UserSerializer

cognito = RealCognito()


class AuthViewSet(ViewSet, CommonViewSet):
    """
    Auth view set
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_path="sign-up")
    def signup(self, request: Request) -> Response:
        """
        The Signup API creates new a user account

        - Check if user already exists (error)
        - Send invitation email (default by cognito)
        """
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email, password = serializer.data["email"], serializer.data["password"]

        if cognito.is_user_existed(email):
            raise AuthError(code="USER_EXISTS")

        # Cognito user create and set password
        cognito_sub = cognito.create_user(email, password)
        cognito.set_user_password(email, password)

        # Create user in database
        User.objects.create(cognito_sub=cognito_sub, email=email)

        return self.created()

    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        Login user
        Note: This API is for admin test login user only
        """
        data = cognito.admin_login_user(
            request.data["email"],
            request.data["password"],
        )
        return self.ok(data)


class UserViewSet(BaseModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False)
    def me(self, request):
        """
        Get current user request

        Args:
            request (Request): The request object

        Returns:
            Response: The response object
        """
        serializer = UserSerializer(request.user)
        return self.ok(serializer.data)
