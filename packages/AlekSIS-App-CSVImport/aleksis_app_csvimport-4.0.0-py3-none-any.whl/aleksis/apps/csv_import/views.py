from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import FormView, ListView

from django_tables2 import SingleTableMixin
from rules.contrib.views import PermissionRequiredMixin

from .forms import ImportTemplateUploadForm
from .models import ImportTemplate
from .tables import ImportTemplateTable


class ImportTemplateListView(PermissionRequiredMixin, SingleTableMixin, ListView):
    """Table of all school terms."""

    model = ImportTemplate
    table_class = ImportTemplateTable
    permission_required = "csv_import.view_importtemplate_rule"
    template_name = "csv_import/import_template/list.html"


class ImportTemplateUploadView(PermissionRequiredMixin, FormView):
    form_class = ImportTemplateUploadForm
    permission_required = "csv_import.upload_importtemplate_rule"
    template_name = "csv_import/import_template/upload.html"

    def form_valid(self, form):
        template_defs = form.cleaned_data["template"]
        try:
            ImportTemplate.update_or_create_templates(template_defs)
        except Exception as e:
            messages.error(
                self.request, _("The import of the import templates failed: \n {}").format(e)
            )
            return self.form_invalid(form)
        messages.success(self.request, _("The import of the import templates was successful."))
        return redirect("import_templates")
