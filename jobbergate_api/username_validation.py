"""
Special validator that restricts email addresses to particular domains if
JOBBERGATE_VALID_EMAIL_DOMAINS is set.

Per https://www.pivotaltracker.com/n/projects/2450975/stories/176081242
"""
import re

from django.core.validators import EmailValidator

from jobbergate_api import settings


if settings.JOBBERGATE_VALID_EMAIL_DOMAINS is None:
    # None (unset) signals that there is no domain restriction
    _DOMAIN_REGEX = re.compile(r".*")
else:
    patterns = [re.escape(d) for d in settings.JOBBERGATE_VALID_EMAIL_DOMAINS.split()]
    _DOMAIN_REGEX = re.compile("|".join(patterns))


class EmailDomainValidator(EmailValidator):
    domain_regex = _DOMAIN_REGEX


validate_email = EmailDomainValidator()
