from collections.abc import Sequence
from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

import pytest

from aleksis.apps.csv_import.models import ImportJob, ImportTemplate, ImportTemplateField
from aleksis.apps.csv_import.util.process import import_csv
from aleksis.core.models import Group, Person, SchoolTerm

pytestmark = pytest.mark.django_db


@pytest.fixture
def import_template():
    def _import_template(model):
        return ImportTemplate.objects.create(
            name="test_template",
            verbose_name="Test Template",
            content_type=ContentType.objects.get_for_model(model),
        )

    return _import_template


@pytest.fixture
def school_term():
    return SchoolTerm.objects.create(
        date_start=date(2020, 1, 1), date_end=date(2020, 12, 31), name="test_school_term"
    )


def _generate_csv_file(data: Sequence[Sequence[str]], heading: Sequence[str]) -> ContentFile:
    txt = ""
    if heading:
        txt += ",".join(heading) + "\n"
    for row in data:
        txt += ",".join(row)
        txt += "\n"
    return ContentFile(txt, name="test_csv_file.csv")


def test_unique_reference_import(import_template, school_term):
    template = import_template(Person)
    ImportTemplateField.objects.create(template=template, field_type="unique_reference", index=0)
    ImportTemplateField.objects.create(template=template, field_type="first_name", index=1)
    ImportTemplateField.objects.create(template=template, field_type="last_name", index=2)

    persons = [["1", "Jane", "Doe"], ["2", "Nathan", "Doe"]]

    csv_file = _generate_csv_file(persons, ["id", "first_name", "last_name"])
    import_job = ImportJob.objects.create(
        template=template, school_term=school_term, data_file=csv_file
    )

    import_csv(import_job)

    qs = Person.objects.all()
    assert qs.count() == len(persons)

    for person in persons:
        assert Person.objects.filter(extended_data__import_ref_csv=person[0]).exists()


def test_json_field_too_nested(school_term, import_template):
    template = import_template(Group)
    ImportTemplateField.objects.create(
        template=template,
        field_type="match",
        index=0,
        args={"db_field": "extended_data__test__test", "json_field": True},
    )
    ImportTemplateField.objects.create(template=template, field_type="name", index=1)

    groups = [
        ["1", "Test Group 1"],
    ]

    csv_file = _generate_csv_file(groups, ["id", "name"])
    import_job = ImportJob.objects.create(
        template=template, school_term=school_term, data_file=csv_file
    )

    with pytest.raises(ValueError, match="The JSON field was too nested."):
        import_csv(import_job)
