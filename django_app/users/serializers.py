from rest_framework import serializers

from django_app.users.models import User

from .validators import PasswordValidator


class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[PasswordValidator()])


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["email", "cognito_sub"]
