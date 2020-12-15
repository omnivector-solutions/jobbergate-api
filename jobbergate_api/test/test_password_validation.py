"""
Test the password validator
"""

from django.core.exceptions import ValidationError
from pytest import fixture, raises

from jobbergate_api import password_validation


@fixture
def validator():
    """
    An instance of the validator
    """
    return password_validation.ASCIIRegexValidator()


def test_validate(validator):
    """
    Do I accept good passwords and produce an error for bad?
    """
    assert validator.validate("iamagoodpassword") is None
    with raises(ValidationError):
        validator.validate("n@ughty!password")
