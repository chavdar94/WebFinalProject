# Generated by Django 4.2.1 on 2023-07-28 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_appuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appuser',
            options={'ordering': ['pk'], 'verbose_name_plural': 'TestingClassMetaVerboseName'},
        ),
    ]
