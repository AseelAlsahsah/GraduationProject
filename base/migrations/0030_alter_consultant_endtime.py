# Generated by Django 4.2 on 2023-05-05 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0029_alter_test_symptoms"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consultant",
            name="endTime",
            field=models.TimeField(
                blank=True, default=datetime.time(15, 10), null=True
            ),
        ),
    ]
