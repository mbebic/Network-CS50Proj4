# Generated by Django 4.0.4 on 2022-12-16 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('yes', 'Following'), ('no', 'Not Following')], max_length=10)),
                ('rel_from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_user', to=settings.AUTH_USER_MODEL)),
                ('rel_to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
