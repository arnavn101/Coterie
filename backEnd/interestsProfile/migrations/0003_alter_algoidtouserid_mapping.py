# Generated by Django 3.2.9 on 2021-11-06 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interestsProfile', '0002_algoidtouserid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algoidtouserid',
            name='mapping',
            field=models.JSONField(null=True),
        ),
    ]
