from typing import ClassVar

from core.models import AbstractBaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from .constants import AssignedSex
from .constants import Gender
from .constants import Race
from .managers import UserManager


class User(AbstractUser, AbstractBaseModel):
    """
    Custom user model with additional fields
    """

    username = None  # type: ignore[assignment]
    password = None  # type: ignore[assignment]

    cognito_sub = models.UUIDField(help_text="User cognito sub value (uuid)")
    email = models.EmailField(blank=False, unique=True)
    dob = models.DateField(
        "Date of birth",
        null=True,
        help_text="Date of birth",
    )
    street_line_1 = models.CharField(
        max_length=255,
        blank=True,
        help_text="First line of an address.",
    )
    street_line_2 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional. Second line of an address.",
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        help_text="City of an address.",
    )
    state = models.CharField(
        max_length=2,
        help_text="State. For US addresses, two letters representing the state.",
        blank=True,
    )
    postal_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{5}(?:-[0-9]{4})?$",
                message="Postal code must be entered in the format: '12345' or '12345-6789'.",
                code="invalid_postal_code",
            ),
        ],
        blank=True,
        help_text="Postal code. We can use the format '12345' or '12345-6789' for extended ZIP codes.",
    )
    country = models.CharField(
        max_length=2,
        blank=True,
        help_text="Two letters representing a country.",
    )
    phone_country_code = models.CharField(
        "Phone country code",
        max_length=5,
        blank=True,
        help_text="Country code (e.g. 1).",
    )
    phone_number = models.CharField(
        "Phone number",
        blank=True,
        max_length=20,
        help_text="Phone number (e.g. 1234567890).",
    )
    gender = models.CharField(
        "Gender",
        choices=Gender.choices(),
        default=Gender.DECLINEDTOANSWER.value,
        max_length=50,
        help_text="User's gender",
    )
    assigned_sex = models.CharField(
        "Assigned Sex",
        choices=AssignedSex.choices(),
        default=AssignedSex.DECLINEDTOANSWER.value,
        help_text="User's assigned sex",
        max_length=50,
    )
    race = models.CharField(
        "Race",
        choices=Race.choices(),
        default=Race.DECLINEDTOANSWER.value,
        help_text="User's race",
        max_length=50,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def full_name_value(self):
        """
        Get full name of the user
        """
        return f"{self.first_name} {self.last_name}".strip()
