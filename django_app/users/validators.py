from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordValidator:
    """
    Validate password
    """

    def __call__(self, value):
        min_length = 8
        if len(value) < min_length:
            raise ValidationError(
                _("Password must be at least %(min_length)d characters long."),
                params={"min_length": min_length},
            )

        if not any(char.isdigit() for char in value):
            raise ValidationError(_("Password must have numeric characters."))

        if not any(char.isalpha() for char in value):
            raise ValidationError(_("Password must contain at least one letter."))

        if not any(char.isupper() for char in value):
            raise ValidationError(_("Password must have uppercase characters."))

        if not any(char.islower() for char in value):
            raise ValidationError(_("Password must have lowercase characters."))

        if not any(char in "!@#$%^&*()-_+=<>?/" for char in value):
            raise ValidationError(_("Password must have symbol characters"))
