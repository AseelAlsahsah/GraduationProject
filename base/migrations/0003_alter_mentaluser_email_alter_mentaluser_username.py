# Generated by Django 4.2 on 2023-04-20 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_disorderscontent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mentaluser",
            name="email",
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="mentaluser",
            name="username",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
