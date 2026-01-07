# Generated manually for Google Meet integration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_notification'),  # Depende de la última migración existente
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='meet_enabled',
            field=models.BooleanField(default=False, verbose_name='Videollamadas habilitadas'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='meet_link',
            field=models.URLField(blank=True, null=True, verbose_name='Enlace de Google Meet'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='meet_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='meet_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_meets', to=settings.AUTH_USER_MODEL),
        ),
    ]
