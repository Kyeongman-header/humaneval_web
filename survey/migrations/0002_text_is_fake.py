# Generated by Django 4.2.2 on 2023-07-08 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="text",
            name="is_fake",
            field=models.BooleanField(default=True),
        ),
    ]
