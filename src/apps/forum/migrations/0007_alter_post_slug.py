# Generated by Django 4.2.1 on 2023-07-01 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_alter_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(editable=False, max_length=250, unique=True),
        ),
    ]
