# Generated by Django 5.1.7 on 2025-03-08 23:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0004_category_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="color",
            field=models.CharField(default="#FFFFFF", max_length=50),
        ),
    ]
