# Generated by Django 4.2.2 on 2023-07-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0004_case_uploaded"),
    ]

    operations = [
        migrations.AddField(
            model_name="text",
            name="korean_text",
            field=models.CharField(default="nan", max_length=20000),
        ),
    ]