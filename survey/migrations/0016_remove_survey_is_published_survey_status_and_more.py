# Generated by Django 4.2.5 on 2023-09-22 01:34

from django.db import migrations, models
import django.utils.timezone
import survey.models.survey


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0015_survey_created_by_user_survey_tenant_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='is_published',
        ),
        migrations.AddField(
            model_name='survey',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Draft'), (2, 'Published'), (3, 'Expired')], db_index=True, default=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='expire_date',
            field=models.DateField(blank=True, default=survey.models.survey.in_duration_day, verbose_name='Survey will not be visible after this date'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='publish_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Survey will only be visible after this date'),
        ),
    ]