# Generated by Django 4.2 on 2023-04-30 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0019_alter_consultant_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultant",
            name="status",
            field=models.BooleanField(null=True),
        ),
    ]