# Generated by Django 4.2.6 on 2023-11-16 04:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Mascota", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mascota",
            name="edad",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
