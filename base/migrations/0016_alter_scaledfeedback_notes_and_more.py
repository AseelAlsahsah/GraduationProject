# Generated by Django 4.2 on 2023-04-26 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0015_alter_disorderscontent_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scaledfeedback",
            name="notes",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="scaledfeedback",
            name="scale",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="session",
            name="sessionDate",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="session",
            name="sessionTime",
            field=models.TimeField(null=True),
        ),
    ]
