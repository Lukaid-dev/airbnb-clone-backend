# Generated by Django 4.1.3 on 2022-12-12 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Amenity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                ("description", models.CharField(max_length=150, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("country", models.CharField(default="Korea", max_length=50)),
                ("city", models.CharField(default="Seoul", max_length=80)),
                ("price", models.PositiveIntegerField()),
                ("rooms", models.PositiveIntegerField()),
                ("toilets", models.PositiveIntegerField()),
                ("description", models.TextField()),
                ("address", models.CharField(max_length=250)),
                ("pet_friednly", models.BooleanField(default=True)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("entire", "Entire Place"),
                            ("private", "Private Room"),
                            ("shared", "Shared Room"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "amenities",
                    models.ManyToManyField(
                        blank=True, related_name="rooms", to="rooms.amenity"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
