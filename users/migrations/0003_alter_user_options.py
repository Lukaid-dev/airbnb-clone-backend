# Generated by Django 4.1.3 on 2022-12-17 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"default_related_name": "users"},
        ),
    ]