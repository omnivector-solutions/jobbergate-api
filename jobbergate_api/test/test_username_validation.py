"""
Test the domain validator for usernames
"""

from django.core.exceptions import ValidationError
from pytest import raises

from jobbergate_api import username_validation


def test_validate_restricted():
    """
    Do I accept good usernames and produce an error for bad?
    """
    assert username_validation.validate_email("goodemail@scania.com") is None
    with raises(ValidationError):
        username_validation.validate_email("n@ughty.email")
