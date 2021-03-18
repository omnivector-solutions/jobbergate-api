"""
Special validator that allows only a-zA-Z0-9

Per https://www.pivotaltracker.com/n/projects/2450975/stories/175993161
"""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


PASSWORD_RX = re.compile(r"^[a-zA-Z0-9]+$")


class ASCIIRegexValidator:
    def validate(self, password, user=None):
        if not PASSWORD_RX.match(password):
            raise ValidationError("This password contains disallowed characters: only a-zA-Z0-9 are allowed")

    def get_help_text(self) -> str:
        return _("Your password must contain only letters a-z (or A-Z) and digits (0-9)")
