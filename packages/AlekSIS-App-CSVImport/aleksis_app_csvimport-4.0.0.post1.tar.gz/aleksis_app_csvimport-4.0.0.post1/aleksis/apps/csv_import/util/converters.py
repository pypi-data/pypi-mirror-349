import re
from collections.abc import Sequence
from datetime import date
from typing import Any, Callable, Union

from django.apps import apps

from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from aleksis.apps.csv_import.settings import SEXES
from aleksis.core import settings
from aleksis.core.util.core_helpers import get_site_preferences


class ConverterRegistry:
    """Registry of known conversion functions."""

    def __init__(self):
        self._converters = {}

    def register(self, func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """Register a conversion function."""
        if func.__name__ in self._converters:
            raise ValueError(f"The converter {func.__name__} is already registered.")
        self._converters[func.__name__] = func

        return func

    def get_from_name(self, name: str) -> Callable[[Any], Any]:
        """Get a conversion function by its name."""
        return self._converters[name]


converter_registry = ConverterRegistry()


@converter_registry.register
def parse_phone_number(value: str) -> Union[PhoneNumber, str]:
    """Parse a phone number."""
    try:
        number = PhoneNumber.from_string(value, settings.PHONENUMBER_DEFAULT_REGION)
        if number.is_valid():
            return number
    except NumberParseException:
        pass
    return ""


@converter_registry.register
def parse_sex(value: str) -> str:
    """Parse sex via SEXES dictionary."""
    value = value.lower()
    if value in SEXES:
        return SEXES[value]

    return ""


@converter_registry.register
def parse_date(value: str) -> Union[date, None]:
    """Parse string date."""
    import dateparser  # noqa

    languages_raw = get_site_preferences()["csv_import__date_languages"]
    languages = languages_raw.split(",") if languages_raw else []
    try:
        return dateparser.parse(value, languages=languages).date()
    except (ValueError, AttributeError):
        return None


@converter_registry.register
def parse_comma_separated_data(value: str) -> Sequence[str]:
    """Parse a string with comma-separated data."""
    return list(filter(lambda v: v, re.split(r"\s*,\s*", value)))


for str_converter in ("capitalize", "lstrip", "strip", "rstrip", "lower", "upper", "title"):
    converter_registry.register(getattr(str, str_converter))


@converter_registry.register
def parse_untis_color(color: str) -> str:
    """Convert a numerical color in BGR order to a standard hex RGB string."""
    color = int(color)
    b, g, r = (color >> 16) & 255, (color >> 8) & 255, color & 255

    return f"#{r:02x}{g:02x}{b:02x}"


@converter_registry.register
def subject_by_short_name(value: str):
    """Get a subject by its shortname."""
    if apps.is_installed("aleksis.apps.cursus"):
        Subject = apps.get_model("cursus", "Subject")
        subject, __ = Subject.objects.get_or_create(short_name=value, defaults={"name": value})
        return subject
