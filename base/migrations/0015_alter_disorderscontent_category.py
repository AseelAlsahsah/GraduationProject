# Generated by Django 4.2 on 2023-04-26 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0014_alter_disorderscontent_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="disorderscontent",
            name="Category",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
