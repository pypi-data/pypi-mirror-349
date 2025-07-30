from django.core.exceptions import PermissionDenied
from django.forms import FileField
from django.utils.translation import gettext as _

import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.converter import convert_form_field, get_form_field_description
from graphene_django.forms.mutation import DjangoFormMutation
from graphene_file_upload.scalars import Upload

from aleksis.core.util.celery_progress import render_progress_page

from ..forms import CSVUploadForm
from ..models import ImportJob, ImportTemplate
from ..tasks import import_csv


@convert_form_field.register(FileField)
def convert_form_field_to_upload(field):
    return Upload(description=get_form_field_description(field), required=field.required)


class ImportTemplateType(DjangoObjectType):
    class Meta:
        model = ImportTemplate
        fields = ["id", "name", "verbose_name"]


class ImportMutation(DjangoFormMutation):
    task_id = graphene.String()

    class Meta:
        form_class = CSVUploadForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):  # noqa: A002
        kwargs = super().get_form_kwargs(root, info, **input)
        kwargs["files"] = {"csv": input.pop("csv")}
        return kwargs

    @classmethod
    def perform_mutate(cls, form, info):
        if not info.context.user.has_perm("csv_import.import_data_rule"):
            raise PermissionDenied()

        import_job = ImportJob(
            school_term=form.cleaned_data["school_term"],
            template=form.cleaned_data["template"],
            data_file=form.files["csv"],
            create=form.cleaned_data["create"],
            additional_params=form.cleaned_data["additional_params"],
        )
        import_job.save()

        result = import_csv.delay(
            import_job.pk,
        )

        render_progress_page(
            info.context,
            result,
            title=_("Progress: Import data from CSV"),
            progress_title=_("Import objects …"),
            success_message=_("The import was done successfully."),
            error_message=_("There was a problem while importing data."),
        )
        return cls(task_id=result.task_id)


class Query(graphene.ObjectType):
    import_templates = graphene.List(ImportTemplateType)

    @staticmethod
    def resolve_import_templates(root, info):
        if not info.context.user.has_perm("csv_import.view_importtemplate_rule"):
            return []
        return ImportTemplate.objects.all()


class Mutation(graphene.ObjectType):
    csv_import = ImportMutation.Field()
