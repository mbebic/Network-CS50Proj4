# Generated by Django 4.0.4 on 2022-12-16 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_relationship'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relationship',
            old_name='rel_from_user',
            new_name='rel_fromuser',
        ),
        migrations.RenameField(
            model_name='relationship',
            old_name='rel_to_user',
            new_name='rel_touser',
        ),
    ]