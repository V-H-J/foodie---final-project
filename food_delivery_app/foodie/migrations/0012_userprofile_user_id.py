# Generated by Django 4.0.6 on 2022-08-05 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodie', '0011_rename_last_name_userprofile_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]