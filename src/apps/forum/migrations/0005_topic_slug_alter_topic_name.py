# Generated by Django 4.2.1 on 2023-06-29 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(default='asd'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
