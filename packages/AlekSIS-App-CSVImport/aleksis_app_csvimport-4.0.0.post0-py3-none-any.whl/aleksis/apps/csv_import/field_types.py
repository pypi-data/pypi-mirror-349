import os
import re
from collections.abc import Sequence
from typing import Any, Callable, ClassVar, Optional, Union
from uuid import uuid4

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db.models import Model
from django.utils.translation import gettext as _

from aleksis.apps.csv_import.util.class_range_helpers import (
    get_classes_per_grade,
    get_classes_per_short_name,
    parse_class_range,
)
from aleksis.apps.csv_import.util.converters import converter_registry
from aleksis.apps.csv_import.util.import_helpers import with_prefix
from aleksis.core.mixins import RegistryObject
from aleksis.core.models import Group, Person, Room, SchoolTerm
from aleksis.core.util.core_helpers import get_site_preferences


class FieldType(RegistryObject):
    verbose_name: ClassVar[str] = ""
    data_type: ClassVar[type] = str
    db_field: ClassVar[str] = ""
    json_field: ClassVar[bool] = False
    converter: ClassVar[Union[str, Sequence[str]] | None] = None
    alternative_db_fields: ClassVar[str | None] = None
    template: ClassVar[str] = ""
    args: dict | None = None

    @classmethod
    def get_data_type(cls) -> type:
        return cls.data_type

    @classmethod
    def get_choices(cls) -> Sequence[tuple[str, str]]:
        """Return choices in Django format."""
        return [(f._class_name, f.verbose_name) for f in cls.registered_objects_list]

    def get_converter(self) -> Callable[[Any], Any]:
        converters_pre = self.get_args().get("converter_pre", [])
        if isinstance(converters_pre, str):
            converters_pre = [converters_pre]
        converters_post = self.get_args().get("converter_post", [])
        if isinstance(converters_post, str):
            converters_post = [converters_post]
        converters = self.get_args().get("converter") or self.converter
        if converters is None:
            converters = []
        elif isinstance(converters, str):
            converters = [converters]
        converters = converters_pre + converters + converters_post

        funcs = [converter_registry.get_from_name(name) for name in converters]

        def _converter_chain(val: Any) -> Any:
            new_val = val
            for func in funcs:
                new_val = func(new_val)
            return new_val

        return _converter_chain

    def get_args(self) -> dict:
        return self.args or {}

    def get_db_field(self) -> str:
        if self.get_args().get("db_field"):
            return self.get_args()["db_field"]
        return self.db_field

    def get_json_field(self) -> bool:
        if self.get_args().get("json_field"):
            return self.get_args()["json_field"]
        return self.json_field

    def get_alternative_db_fields(self) -> list[str]:
        if self.get_args().get("alternative_db_fields"):
            return self.get_args()["alternative_db_fields"]
        return self.alternative_db_fields or []

    def get_column_name(self) -> str:
        """Get column name for use in Pandas structures."""
        if self.get_args().get("column_name"):
            return self.get_args()["column_name"]
        return self.column_name

    def get_template(self) -> str:
        if self.get_args().get("template"):
            return self.get_args()["template"]
        return self.template or ""

    def __init__(
        self, school_term: SchoolTerm, additional_params: dict[str, any], base_path: str, **kwargs
    ):
        self.school_term = school_term
        self.additional_params = additional_params
        self.base_path = os.path.realpath(base_path)
        self.column_name = f"col_{uuid4()}"
        self.args = kwargs


class MatchFieldType(FieldType):
    """Field type for getting an instance."""

    _class_name = "match"
    priority: int = 1

    def get_priority(self):
        return self.get_args().get("priority", "") or self.priority


class ConnectedMatchFieldType(MatchFieldType):
    """Set multiple conditions for matching an object while importing."""

    _class_name = "connected_match"

    conditions: dict[str, any] = None

    def get_conditions(self):
        return self.get_args().get("conditions", None) or self.conditions or {}


class DirectMappingFieldType(FieldType):
    """Set value directly in DB."""

    _class_name = "direct_mapping"


class ProcessFieldType(FieldType):
    """Field type with custom logic for importing."""

    run_before_save: bool = False

    def process(self, instance: Model, value):
        pass


class IgnoreFieldType(FieldType):
    """Ignore the data in this field."""

    _class_name = "ignore"
    verbose_name = _("Ignore data in this field")


class RegExFieldType(ProcessFieldType):
    """Field type to apply a regex transformation."""

    _class_name = "reg_ex"
    data_type = str
    reg_ex: ClassVar[str] = ""
    fail_if_no_match: ClassVar[bool] = False

    def get_reg_ex(self):
        return self.reg_ex or self.get_args().get("reg_ex", "")

    def get_fail_if_no_match(self):
        return self.fail_if_no_match or self.get_args().get("fail_if_no_match", False)

    def process(self, instance: Model, value):
        match = re.fullmatch(self.get_reg_ex(), value)
        if match:
            for key, item in match.groupdict().items():
                setattr(instance, key, item)
            instance.save()
        elif self.get_fail_if_no_match():
            raise IndexError(
                _("No match on {} for regular expression {} found.").format(
                    value, self.get_reg_ex()
                )
            )


class ConverterRegExFieldType(FieldType):
    """Field type with custom converter to transform value with a reg ex."""

    _class_name = "converter_reg_ex"
    reg_ex = ""

    def get_reg_ex(self):
        return self.reg_ex or self.get_args().get("reg_ex", "")

    def get_converter(self) -> Optional[Callable]:
        def regex_converter(value: str):
            match = re.match(self.get_reg_ex(), value)
            if match:
                return match.group(1)
            return value

        return regex_converter


class ConverterIgnoreRegExFieldType(ConverterRegExFieldType, IgnoreFieldType):
    """Field type with custom converter to transform value with a reg ex.

    The value from this field can be used in virtual fields then.
    """

    _class_name = "converter_ignore_reg_ex"


class UniqueReferenceFieldType(MatchFieldType):
    _class_name = "unique_reference"
    verbose_name = _("Unique reference")
    db_field = "extended_data__import_ref_csv"
    priority = 10
    json_field = True


class NameFieldType(DirectMappingFieldType):
    _class_name = "name"
    verbose_name = _("Name")
    db_field = "name"
    alternative_db_fields = ["short_name"]


class FirstNameFieldType(DirectMappingFieldType):
    _class_name = "first_name"
    verbose_name = _("First name")
    db_field = "first_name"


class LastNameFieldType(DirectMappingFieldType):
    _class_name = "last_name"
    verbose_name = _("Last name")
    db_field = "last_name"


class AdditionalNameFieldType(DirectMappingFieldType):
    _class_name = "additional_name"
    verbose_name = _("Additional name")
    db_field = "additional_name"


class ShortNameFieldType(MatchFieldType):
    _class_name = "short_name"
    verbose_name = _("Short name")
    priority = 8
    db_field = "short_name"
    alternative_db_fields = ["name", "first_name", "last_name"]


class EmailFieldType(MatchFieldType):
    _class_name = "email"
    verbose_name = _("Email")
    db_field = "email"
    priority = 12

    def get_converter(self) -> Optional[Callable]:
        if "email_domain" in self.get_args():

            def add_domain_to_email(value: str) -> str:
                if "@" in value:
                    return value
                else:
                    return f"{value}@{self.get_args()['email_domain']}"

            return add_domain_to_email
        return super().get_converter()


class DateOfBirthFieldType(DirectMappingFieldType):
    _class_name = "date_of_birth"
    verbose_name = _("Date of birth")
    db_field = "date_of_birth"
    converter = "parse_date"


class SexFieldType(DirectMappingFieldType):
    _class_name = "sex"
    verbose_name = _("Sex")
    db_field = "sex"
    converter = "parse_sex"


class StreetFieldType(DirectMappingFieldType):
    _class_name = "street"
    verbose_name = _("Street")
    db_field = "street"


class HouseNumberFieldType(DirectMappingFieldType):
    _class_name = "housenumber"
    verbose_name = _("Housenumber")
    db_field = "housenumber"


class StreetAndHouseNumberFieldType(RegExFieldType):
    _class_name = "street_housenumber"
    verbose_name = _("Street and housenumber")
    reg_ex = r"^(?P<street>[\w\s]{3,})\s+(?P<housenumber>\d+\s*[a-zA-Z]*)$"


class PostalCodeFieldType(DirectMappingFieldType):
    _class_name = "postal_code"
    verbose_name = _("Postal code")
    db_field = "postal_code"


class PlaceFieldType(DirectMappingFieldType):
    _class_name = "place"
    verbose_name = _("Place")
    db_field = "place"


class PhoneNumberFieldType(DirectMappingFieldType):
    _class_name = "phone_number"
    verbose_name = _("Phone number")
    db_field = "phone_number"
    converter = "parse_phone_number"


class MobileNumberFieldType(DirectMappingFieldType):
    _class_name = "mobile_number"
    verbose_name = _("Mobile number")
    db_field = "mobile_number"
    converter = "parse_phone_number"


class DepartmentsFieldType(ProcessFieldType):
    _class_name = "departments"
    verbose_name = _("Comma-seperated list of departments")
    converter = "parse_comma_separated_data"

    def process(self, instance: Model, value, short_name=True):
        first_attr = "short_name" if short_name else "name"
        second_attr = "name" if short_name else "short_name"

        with_cursus = apps.is_installed("aleksis.apps.cursus")
        if with_cursus:
            Subject = apps.get_model("cursus", "Subject")

        group_type = get_site_preferences()["csv_import__group_type_departments"]
        group_prefix = get_site_preferences()["csv_import__group_prefix_departments"]

        groups = []
        for subject_name in value:
            if with_cursus:
                # Get department subject
                subject, __ = Subject.objects.get_or_create(
                    **{first_attr: subject_name}, defaults={second_attr: subject_name}
                )
                name = subject.name
                short_name = subject.short_name
            else:
                name = subject_name
                short_name = subject_name

            # Get department group
            group, __ = Group.objects.get_or_create(
                group_type=group_type,
                short_name=short_name,
                defaults={"name": with_prefix(group_prefix, name)},
            )
            if with_cursus:
                group.extended_data["subject_id"] = subject
            group.save()

            groups.append(group)

        instance.member_of.add(*groups)


class DepartmentsShortNameFieldType(DepartmentsFieldType):
    """Import a comma-separated list of departments by short name."""

    _class_name = "departments"
    verbose_name = _("Comma-separated list of departments (short name of subjects)")

    def process(self, instance: Model, value):
        return super().process(instance, value, short_name=True)


class DepartmentsNameFieldType(DepartmentsFieldType):
    _class_name = "departments_name"
    verbose_name = _("Comma-separated list of departments (long name of subjects)")

    def process(self, instance: Model, value):
        return super().process(instance, value, short_name=False)


class ClassRangeFieldType(ProcessFieldType):
    _class_name = "class_range"
    verbose_name = _("Class range (e. g. 7a-d)")

    def __init__(
        self, school_term: SchoolTerm, additional_params: dict[str, any], base_path: str, **kwargs
    ):
        # Prefetch class groups
        self.classes_per_short_name = get_classes_per_short_name(school_term)
        self.classes_per_grade = get_classes_per_grade(self.classes_per_short_name.keys())

        super().__init__(school_term, additional_params, base_path, **kwargs)

    def process(self, instance: Model, value):
        classes = parse_class_range(
            self.classes_per_short_name,
            self.classes_per_grade,
            value,
        )
        instance.parent_groups.set(classes)


class PrimaryGroupByShortNameFieldType(ProcessFieldType):
    _class_name = "primary_group_short_name"
    verbose_name = _("Short name of the person's primary group")

    def process(self, instance: Model, value):
        if not value:
            return
        group, __ = Group.objects.get_or_create(
            short_name__iexact=value,
            school_term=self.school_term,
            defaults={"short_name": value, "name": value},
        )
        instance.primary_group = group
        instance.member_of.add(group)
        instance.save()


class PrimaryGroupOwnerByShortNameFieldType(ProcessFieldType):
    _class_name = "primary_group_owner_short_name"
    verbose_name = _("Short name of an owner of the person's primary group")

    def process(self, instance: Model, value):
        if instance.primary_group:
            owners = Person.objects.filter(short_name=value)
            instance.primary_group.owners.set(owners)


class GroupOwnerByShortNameFieldType(ProcessFieldType):
    _class_name = "group_owner_short_name"
    verbose_name = _("Short name of a single group owner")

    def process(self, instance: Model, short_name: str):
        if not short_name:
            return
        group_owner, __ = Person.objects.get_or_create(
            short_name=short_name,
            defaults={"first_name": "?", "last_name": short_name},
        )
        if self.get_args().get("clear", False):
            instance.owners.set([group_owner])
        else:
            instance.owners.add(group_owner)


class GroupOwnerByFullNameFieldType(ProcessFieldType):
    """Set a group owner by its full name."""

    _class_name = "group_owner_full_name"
    verbose_name = _("Full name of a single group owner (last name, first name)")

    def process(self, instance: Model, value: str):
        if not value:
            return
        last_name, first_name = re.split(r"\s*,\s*", value)
        group_owner, __ = Person.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
        )
        if self.get_args().get("clear", False):
            instance.owners.set([group_owner])
        else:
            instance.owners.add(group_owner)


class GroupMemberByFullNameFieldType(ProcessFieldType):
    """Set a group member by its full name."""

    _class_name = "group_member_full_name"
    verbose_name = _("Full name of a single group member (last name, first name)")

    def process(self, instance: Model, value: str):
        if not value:
            return
        last_name, first_name = re.split(r"\s*,\s*", value)
        group_member, __ = Person.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
        )
        if self.get_args().get("clear", False):
            instance.members.set([group_member])
        else:
            instance.members.add(group_member)


class GroupMemberByUniqueReferenceFieldType(ProcessFieldType):
    """Set a group member by its unique reference (import_ref_csv)."""

    _class_name = "group_member_unique_reference"
    verbose_name = _("Unique reference of a single group member (import_ref_csv)")

    def process(self, instance: Model, value: str):
        if not value:
            return
        try:
            group_member = Person.objects.get(extended_data__import_ref_csv=value)
            if self.get_args().get("clear", False):
                instance.members.set([group_member])
            else:
                instance.members.add(group_member)
        except Person.DoesNotExist:
            pass


class GroupMembershipByShortNameFieldType(ProcessFieldType):
    _class_name = "group_membership_short_name"
    verbose_name = _("Short name of the group the person is a member of")

    def process(self, instance: Model, short_name: str):
        if not short_name:
            return
        try:
            group = Group.objects.get(short_name=short_name, school_term=self.school_term)
            instance.member_of.add(group)
        except Group.DoesNotExist:
            pass


class ParentGroupByShortNameFieldType(ProcessFieldType):
    _class_name = "parent_group_short_name"
    verbose_name = _("Short name of the group's parent group")

    def process(self, instance: Model, value):
        if not value:
            return
        group, __ = Group.objects.get_or_create(
            short_name=value, school_term=self.school_term, defaults={"name": value}
        )
        instance.parent_groups.add(group)
        instance.save()


class MemberOfByNameFieldType(ProcessFieldType):
    _class_name = "member_of_by_name"
    verbose_name = _("Name of a group the person is a member of")

    def process(self, instance: Model, value):
        if not value:
            return
        group, __ = Group.objects.get_or_create(name=value, school_term=self.school_term)
        instance.member_of.add(group)
        instance.save()


class ChildByUniqueReference(ProcessFieldType):
    _class_name = "child_by_unique_reference"
    verbose_name = _("Child by unique reference (from students import)")

    def process(self, instance: Model, value):
        if not value:
            return
        try:
            child = Person.objects.get(import_ref_csv=value)
            instance.children.add(child)
        except Person.DoesNotExist:
            pass


class FileFieldType(ProcessFieldType):
    """Field type that stores a referenced file on a file field."""

    def process(self, instance: Model, value: str):
        # Get target FileField and save content
        field_name = self.get_db_field()
        file_field = getattr(instance, field_name)

        if value:
            # Test path for unwanted path traversal
            abs_path = os.path.realpath(value)
            if not self.base_path == os.path.commonpath((self.base_path, abs_path)):
                raise ValueError(f"Disallowed path traversal importing file from {value}")

            with open(abs_path, "rb") as f:
                file_field.save(os.path.basename(abs_path), File(f))
        else:
            # Clear the file field
            file_field.delete()

        instance.save()


class AvatarFieldType(FileFieldType):
    _class_name = "avatar"
    db_field = "avatar"


class PhotoFieldType(FileFieldType):
    _class_name = "photo"
    db_field = "photo"


class GroupByShortNameFieldType(ProcessFieldType):
    _class_name = "group_by_short_name"
    verbose_name = _("Short name of a related group (groups)")

    def process(self, instance: Model, value):
        if value:
            group, __ = Group.objects.get_or_create(
                short_name=value, school_term=self.school_term, defaults={"name": value}
            )
            instance.groups.add(group)
            instance.save()


class TeacherByShortNameFieldType(ProcessFieldType):
    _class_name = "teacher_by_short_name"
    verbose_name = _("Short name of a related teacher (teachers)")

    def process(self, instance: Model, value):
        if value:
            person, __ = Person.objects.get_or_create(
                short_name=value, defaults={"last_name": value, "first_name": "?"}
            )
            instance.teachers.add(person)
            instance.save()


class DefaultRoomByShortNameFieldType(ProcessFieldType):
    _class_name = "default_room_by_short_name"
    verbose_name = _("Short name of the default room")

    def process(self, instance: Model, value):
        if not value:
            instance.default_room = None
        else:
            room, __ = Room.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.default_room = room
        instance.save()


class LessonQuotaFieldType(DirectMappingFieldType):
    _class_name = "lesson_quota"
    verbose_name = _("Lesson quota")
    db_field = "lesson_quota"
    data_type = int


class RoomByShortNameFieldType(ProcessFieldType):
    _class_name = "room_by_short_name"
    verbose_name = _("Short name of a related room (rooms)")

    def process(self, instance: Model, value):
        if value:
            room, __ = Room.objects.get_or_create(short_name=value, defaults={"name": value})
            instance.rooms.add(room)
            instance.save()


class UsernameFieldType(ProcessFieldType):
    _class_name = "username"
    verbose_name = _("Username")
    run_before_save = True
    converter = "strip"

    def process(self, instance: Model, value):
        if instance.user:
            return

        if value and not get_user_model().objects.filter(username=value).exists():
            user = get_user_model().objects.create_user(value)
            instance.user = user
