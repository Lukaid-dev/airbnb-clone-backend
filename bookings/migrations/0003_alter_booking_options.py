# Generated by Django 4.1.3 on 2022-12-17 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_booking_experience_time_booking_guests"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="booking",
            options={"default_related_name": "bookings"},
        ),
    ]