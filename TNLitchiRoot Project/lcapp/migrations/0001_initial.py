# Generated by Django 4.1.7 on 2023-02-21 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("affiliate", models.CharField(max_length=45)),
                ("sector", models.CharField(max_length=45)),
                ("career", models.CharField(max_length=20)),
                ("prefer", models.TextField()),
                ("sdate", models.DateField()),
                ("edate", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Seeker",
            fields=[
                ("email", models.TextField(primary_key=True, serialize=False)),
                ("pwd", models.CharField(max_length=30)),
                ("name", models.CharField(max_length=30)),
                ("phone", models.CharField(max_length=50)),
                ("gender", models.CharField(max_length=6)),
                ("cdate", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Apply",
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
                ("resume", models.FileField(blank=True, upload_to="%Y/")),
                (
                    "acompany",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="lcapp.company"
                    ),
                ),
                (
                    "aseeker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="lcapp.seeker"
                    ),
                ),
            ],
        ),
    ]