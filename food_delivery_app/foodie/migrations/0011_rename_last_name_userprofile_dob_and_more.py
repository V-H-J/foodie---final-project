# Generated by Django 4.0.6 on 2022-08-05 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0010_userprofile_email_id_userprofile_phone_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='last_name',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_name',
            new_name='favorite_food',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='email_id',
            new_name='favorite_restaurant',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='phone',
            new_name='gender',
        ),
    ]
