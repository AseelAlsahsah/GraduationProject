# Generated by Django 4.2 on 2023-04-26 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0013_rename_feedback_websitefeedback_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="disorderscontent",
            name="Category",
            field=models.CharField(default="Depression", max_length=100),
        ),
    ]
