# Generated by Django 4.2.1 on 2023-07-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_appuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='remember_me',
            field=models.BooleanField(default=False),
        ),
    ]
