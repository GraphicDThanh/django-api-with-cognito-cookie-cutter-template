from typing import TYPE_CHECKING
from typing import Any

from django.contrib.auth.models import UserManager as DjangoUserManager

from django_app.core.exceptions import UnauthorizedError

if TYPE_CHECKING:
    from .models import User  # noqa: F401


class UserManager(DjangoUserManager["User"]):
    """Custom manager for the User model."""

    def get_or_create_for_cognito(self, payload: dict[str, Any]):  # typing: ignore
        """
        Get user with cognito id
        """
        cognito_id: str = payload["cognito:username"]
        try:
            return self.get(cognito_sub=cognito_id)
        except self.model.DoesNotExist as e:
            raise UnauthorizedError(code="INVALID_CREDENTIALS") from e
