# Generated by Django 4.1.3 on 2022-12-17 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("direct_messages", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chanttingroom",
            options={"default_related_name": "chantting_rooms"},
        ),
        migrations.AlterModelOptions(
            name="message",
            options={"default_related_name": "messages"},
        ),
    ]