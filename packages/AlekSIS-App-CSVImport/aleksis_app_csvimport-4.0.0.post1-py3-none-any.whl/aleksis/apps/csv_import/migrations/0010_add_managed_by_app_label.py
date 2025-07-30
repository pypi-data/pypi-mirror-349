import aleksis.core.managers
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csv_import', '0009_importjob_create_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='importtemplate',
            name='managed_by_app_label',
            field=models.CharField(blank=True, editable=False, max_length=255, verbose_name='App label of app responsible for managing this instance'),
        ),
        migrations.AddField(
            model_name='importtemplatefield',
            name='managed_by_app_label',
            field=models.CharField(blank=True, editable=False, max_length=255, verbose_name='App label of app responsible for managing this instance'),
        ),
        migrations.AddField(
            model_name='importjob',
            name='managed_by_app_label',
            field=models.CharField(blank=True, editable=False, max_length=255, verbose_name='App label of app responsible for managing this instance'),
        ),
    ]
