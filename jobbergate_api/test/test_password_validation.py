"""
Test the password validator
"""

from django.core.exceptions import ValidationError
from pytest import fixture, raises

from jobbergate_api import password_validation


@fixture
def validator() -> password_validation.ASCIIRegexValidator:
    """
    An instance of the validator
    """
    return password_validation.ASCIIRegexValidator()


def test_validate(validator: password_validation.ASCIIRegexValidator):
    """
    Do I accept good passwords and produce an error for bad?
    """
    assert validator.validate("iamagoodpassword") is None
    with raises(ValidationError):
        validator.validate("n@ughty!password")


def test_get_help_text(validator: password_validation.ASCIIRegexValidator):
    """
    Do I have a help text?
    """
    assert type(validator.get_help_text()) is str
