# Generated by Django 4.1.3 on 2022-12-17 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medias", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="photo",
            options={"default_related_name": "photos"},
        ),
        migrations.AlterModelOptions(
            name="video",
            options={"default_related_name": "videos"},
        ),
    ]
