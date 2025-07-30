import codecs
import logging
from collections.abc import Sequence
from typing import Any

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext as _

from aleksis.core.mixins import ExtensibleModel
from aleksis.core.models import Group, GroupType, SchoolTerm

from .field_types import FieldType

logger = logging.getLogger(__name__)


class ImportTemplate(ExtensibleModel):
    from_default = models.BooleanField(default=False)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_("Content type"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    verbose_name = models.CharField(max_length=255, verbose_name=_("Name"))

    has_header_row = models.BooleanField(
        default=True, verbose_name=_("Has the CSV file an own header row?")
    )
    has_index_col = models.BooleanField(
        default=False, verbose_name=_("Has the CSV file an own index column?")
    )
    separator = models.CharField(
        max_length=255,
        default=",",
        verbose_name=_("CSV separator"),
        help_text=_("For whitespace use \\\\s+, for tab \\\\t"),
    )
    quotechar = models.CharField(
        max_length=255,
        default='"',
        verbose_name=_("CSV quote character"),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Base group"),
        help_text=_(
            "If imported objects are persons, they all will be members of this group after import."
        ),
    )
    group_type = models.ForeignKey(
        GroupType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Group type"),
        help_text=_(
            "If imported objects are groups, they all will get this group type after import."
        ),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Import template")
        verbose_name_plural = _("Import templates")

    def __str__(self):
        return self.verbose_name

    def save(self, *args, **kwargs):
        if self.content_type.model != "person":
            self.group = None
        if self.content_type.model != "group":
            self.group_type = None
        super().save(*args, **kwargs)

    @property
    def parsed_separator(self):
        return codecs.escape_decode(bytes(self.separator, "utf-8"))[0].decode("utf-8")

    @property
    def parsed_quotechar(self):
        return codecs.escape_decode(bytes(self.quotechar, "utf-8"))[0].decode("utf-8")

    @classmethod
    def update_or_create(
        cls,
        model: Model,
        name: str,
        verbose_name: str,
        extra_args: dict,
        fields: Sequence[tuple[FieldType, dict[str, Any], bool, str]],
    ):
        """Update or create an import template in database."""
        ct = ContentType.objects.get_for_model(model)
        template, updated = cls.objects.update_or_create(
            name=name,
            defaults={"verbose_name": verbose_name, "content_type": ct, **extra_args},
        )

        i = 0
        for i, field in enumerate(fields):
            field_type, args, virtual, virtual_tmpl = field
            ImportTemplateField.objects.update_or_create(
                template=template,
                index=i,
                defaults={
                    "field_type": field_type._class_name,
                    "args": args,
                    "virtual": virtual,
                    "virtual_tmpl": virtual_tmpl,
                },
            )

        ImportTemplateField.objects.filter(template=template, index__gt=i).delete()

        return template

    @classmethod
    def update_or_create_templates(cls, template_defs, from_default: bool = False):
        """Update or create import templates."""
        for name, defs in template_defs.items():
            try:
                model = apps.get_model(defs["model"])

                fields = []
                for field_definition in defs["fields"]:
                    if isinstance(field_definition, str):
                        field_type_name = field_definition
                        virtual = False
                        template = ""
                        args = {}
                    else:
                        field_type_name = field_definition.pop("field_type")
                        virtual = field_definition.pop("virtual", False)
                        template = field_definition.pop("template", "")
                        args = field_definition
                    field_type = FieldType.get_object_by_name(field_type_name)
                    if not field_type:
                        raise ValueError(f"There is no field type with the name {field_type_name}")
                    fields.append((field_type, args, virtual, template))

                extra_args = defs.get("extra_args", {})
                extra_args["from_default"] = from_default

                cls.update_or_create(
                    model,
                    name=name,
                    verbose_name=defs.get("verbose_name", ""),
                    extra_args=extra_args,
                    fields=fields,
                )
            except (LookupError, ValueError):
                logger.warning(f"Skip import of CSV import template {name}.")
                continue


class ImportTemplateField(ExtensibleModel):
    index = models.IntegerField(verbose_name=_("Index"))
    template = models.ForeignKey(
        ImportTemplate,
        models.CASCADE,
        verbose_name=_("Import template"),
        related_name="fields",
    )
    field_type = models.CharField(
        max_length=255,
        verbose_name=_("Field type"),
        choices=FieldType.get_choices(),
    )
    args = models.JSONField(verbose_name=_("Optional arguments passed to field type"), default={})

    virtual = models.BooleanField(verbose_name=_("Virtual field"), default=False, null=False)
    virtual_tmpl = models.TextField(
        verbose_name=_("Django template to generate virtual field from"), blank=True
    )

    class Meta:
        ordering = ["template", "index"]
        unique_together = ["template", "index"]
        verbose_name = _("Import template field")
        verbose_name_plural = _("Import template fields")

    def __str__(self):
        return f"{self.template}/{self.index}: {self.field_type}"

    @property
    def field_type_class(self):
        field_type = FieldType.get_object_by_name(self.field_type)
        return field_type


class ImportJob(ExtensibleModel):
    """Job definition for one import, to track import history and files."""

    template = models.ForeignKey(
        ImportTemplate,
        on_delete=models.CASCADE,
        verbose_name=_("Import template"),
        related_name="import_jobs",
    )
    data_file = models.FileField(upload_to="csv_import/")
    school_term = models.ForeignKey(
        SchoolTerm,
        on_delete=models.CASCADE,
        verbose_name=_("School term"),
        related_name="import_jobs",
        blank=True,
        null=True,
    )
    create = models.BooleanField(default=True, verbose_name=_("Create new objects if necessary"))
    additional_params = models.JSONField(verbose_name=_("Additional parameters"), default=dict)

    class Meta:
        verbose_name = _("Import job")
        verbose_name_plural = _("Import jobs")

    def __str__(self):
        return f"{self.template}#{self.pk}"
